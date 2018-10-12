"""
Main
"""
import uuid
import sys
from twisted.internet import reactor
from twisted.internet import task
from tom.common import log
from tom.ocpp import message
from tom.ocpp import error
from tom.storage import base as storage
from tom.soap import service as soap
from tom.json import service as websocket
from tom.common.utils import now, duration


def charge_point_call_done(response, request, sender):
    """
    Обработчик ответа ЦС на запрос от ЗС
    ЗС -> CALL конвертер -> CALL ЦС -> ЦС RESULT/ERROR -> конвертер RESULT/ERROR -> charge_point_call_done
    response - ответ полученный от ЦS
    request - оригинальный запрос
    sender - функция для отправки ответа. sender формируется на сторону SOAP-сервера и содержит все
    необходимые данные для отправки ответа. Единственный аргумент функции - сообщение с ответом
    Задача методы - подготовить ответ исходя из запроса и полученного ответа от ЦС, затем
    передать для отправки
    """
    try:
        if response is not None:
            msg_id = response['MessageID']
            response['MessageID'] = str(uuid.uuid4())
            response['RelatesTo'] = msg_id
            response['Action'] = request['Action']
        sender(response)
    except:
        pass


def charge_point_message(charge, msg, sender):
    """
    Обработчик входящего вызова от зарядной станции
    ЗС -> CALL конвертер -> charge_point_message
    Получает уведомление от SOAP-сервера.
    msg - запрос от станции
    sender - функция с 1 аргументов для отправки ответа. Аргумент - ответ на запрос
    В случае успеха возвращает True
    """
    msg_id = msg['MessageID']
    msg_type = msg['Type']
    if msg_type == message.CALL:
        # Вызов от зарядной станции
        address = msg['From']
        WS.send(charge, msg,
                make_connection=True)

        def on_done(response): return charge_point_call_done(
            response, msg, sender)
        STORAGE.add(msg_id, msg, on_done)
        return True
    elif msg_type in (message.RESULT,  message.ERROR):
        # Ответ от зарядной станции
        relates_id = msg['RelatesTo']
        STORAGE.done(relates_id, msg)
        return True

    return False


def charge_point_expired(charge):
    """ Обработчик слишком длительного мочания со стороны зарядной станции. """
    log.info('APP:[{0}] is expired'.format(charge))
    WS.drop(charge)
    res = charge_point_clean(charge)
    if res > 0:
        log.info('APP:[{0}] {1} record(s) were removed'.format(charge, res))


def charge_point_clean(charge):
    """ Удаление сообщений, связанных с зарядной станцией """
    def name_selector(record):
        # Функция для выбора записей по имени станции
        if record.message['chargeBoxIdentity'] == charge:
            return True
        return False

    # Очистить связанные сообщения и закрыть подключение по WS
    start_size = STORAGE.count()
    STORAGE.vacuum(name_selector)
    end_size = STORAGE.count()

    return start_size - end_size


def central_system_call_done(response, request, charge):
    """
    Обработчик ответа ЗС на  запрос от ЦС
    ЦС -> CALL конвертер -> CALL ЗС -> ЗС RESULT/ERROR -> конвертер RESULT/ERROR -> central_system_call_done
    response - ответ на запроса
    request - оригинальный запрос
    charge - имя зарядной станции, которой был отправлен запрос
    """
    msg_id = request['MessageID']
    response['MessageID'] = msg_id
    WS.send(charge, response)


def central_system_message(charge, msg, sender):
    """
    Получение сообщения от ЦС
    Общий обработчик. Будет вызван при получении вызова, результата или ошибки
    """
    msg_type = msg['Type']
    msg_id = msg['MessageID']
    # В данном обработчике возможно получение 3-х типов сообщений:
    # - вызов
    # - результат вызова
    # - ошибка
    # Получении вызова:
    # Если сообщение отправлено к станции, то задаем реакцию на получение ответа и
    # добавляем его к отслеживаемым сообщениям.
    # Если отправить не получилось, уведомляем ЦС.
    # Получение результата: уведомляем очередь сообщений о получении результата.
    # Получение ошибки: уведомляем очередь сообщений о получении ошибки
    if msg_type == message.CALL:
        # Вызов
        res = SOAP.send(charge, msg)
        if res:
            # Успешное отправление
            def on_done(response): return central_system_call_done(
                response, msg, charge)
            STORAGE.add(msg_id, msg, on_done)
        else:
            # Ошибки отправки
            response = error.create(msg['MessageID'], 'NotRespond')
            WS.send(charge, response)

    elif msg_type == message.RESULT:
        # Результат
        STORAGE.done(msg_id, msg)
    elif msg_type == message.ERROR:
        # Ошибка
        STORAGE.done(msg_id, None)


def central_system_link_up(charge):
    log.info('APP:[{0}] link is up'.format(charge))

    def name_selector(record):
        # Функция для выбора записей по имени станции
        if record.message['chargeBoxIdentity'] == charge:
            return True
        return False

    messages = STORAGE.select(name_selector)
    size = len(messages)
    for msg in messages:
        WS.send(charge, msg)

    if size > 0:
        log.info(
            'APP:[{0}] flush {1} record(s) from storage'.format(charge, size))


def central_system_link_down(charge):
    log.info('APP:[{0}] link is down'.format(charge))
    res = charge_point_clean(charge)
    if res > 0:
        log.info('APP:[{0}] record(s) were removed'.format(res))


def message_deleter(record):
    """
    Генератор сообщений. Вызывается для каждого сообщения, удаляемого из очереди по таймаута / отключению ЗС
    Возвращает сгенерированный ответ на удаляемый запрос
    """
    try:
        msg_id = record.message['MessageID']
        charge = record.message['chargeBoxIdentity']
        response = error.create(msg_id, 'NotRespond')
        return response
    except Exception as e:
        log.error('APP: storage {0}'.format(e))


def vacuum(expired_timeout):
    """
    проверка очередисообщений и очистка от старых записей
    """

    def timed_selector(record, timeout, current):
        # Функция выбора по времени обновления
        if duration(current, record.timestamp) >= timeout:
            return True
        return False

    start_size = STORAGE.count()
    log.debug('APP: message storage size is {0}'.format(start_size))

    def old_messages(r): return timed_selector(r, expired_timeout, now())
    STORAGE.vacuum(old_messages)
    end_size = STORAGE.count()
    if start_size > end_size:
        log.info('APP: {0} record(s) were removed from storage. Current size is {1}'.format(
            start_size - end_size, end_size))


def read_arguments():
    """
    Чтение аргументов командной строки
    """
    result = DEFAULTS
  #  {'interface':'0.0.0.0',
  #            'port': 8080,
  #            'loglevel': 'error',
  #            'logfile':None,
  #            'inactive-timeout': 90}

    try:
        cnt = 0
        for arg in sys.argv:
            if arg.find('--interface') >= 0:
                _, iface = arg.split("=")
                result['interface'] = iface
            elif arg.find('--port') >= 0:
                _, port = arg.split("=")
                result['port'] = int(port)
            elif arg.find('--inactive-timeout') >= 0:
                _, timeout = arg.split("=")
                result['inactive-timeout'] = float(timeout)
            elif arg.find('--url') >= 0:
                _, url = arg.split("=")
                result['url'] = url
            elif arg.find('--loglevel') >= 0:
                _, level = arg.split("=")
                result['loglevel'] = level
            elif arg.find('--logfile') >= 0:
                _, level = arg.split("=")
                result['logfile'] = level
            elif arg.find('--help') >= 0:
                raise Exception()
            else:
                if cnt != 0:
                    print('Unknown argument {0}'.format(arg))
                    raise Exception()
            cnt += 1
        if not result['url']:
            raise Exception()

    except:
        usage()
        sys.exit()

    return result


def usage():
    print('\nOCPP(SOAP) <-> OCPP(JSON) converter')
    print('\nParameters:')
    print(
        '\t--interface - interface name for server\'s binding. {0} by default'.format(DEFAULTS['interface']))
    print(
        '\t--port - port number for SOAP server. {0} by default'.format(DEFAULTS['port']))
    print(
        '\t--loglevel - logging details [debug,info,warning,error]. {0} by default'.format(DEFAULTS['loglevel']))
    print(
        '\t--logfile - file to save log data. {0} by default'.format(DEFAULTS['logfile']))
    print('\t--inactive-timeout - connection will be dropped if no messages were received during this timeout. {0} by default'.format(
        DEFAULTS['inactive-timeout']))
    print('\t--help - print help')
    print('\nExample:')
    print('\tpython main.py --loglevel=debug --port=8888 --url=ws://192.168.56.101:8080/steve/websocket/CentralSystemService')


if __name__ == '__main__':
    DEFAULTS = {'interface': '0.0.0.0',
                'port': 8080,
                'loglevel': 'error',
                'logfile': None,
                'inactive-timeout': 90}

    VACUUM_TIMEOUT = 10
    ARGS = read_arguments()
    URL = ARGS['url']
    PORT = ARGS['port']
    TIMEOUT = ARGS['inactive-timeout']
    LOGLEVEL = ARGS['loglevel']
    LOGFILE = ARGS['logfile']
    IFACE = ARGS['interface']

    STORAGE = storage.MessageStorage(deleter=message_deleter)
    SOAP = soap.Service(
        interface=IFACE,
        port=PORT,
        on_message=charge_point_message,
        on_expire=charge_point_expired,
        inactive_timeout=TIMEOUT)

    WS = websocket.Service(url=URL,
                           on_open=central_system_link_up,
                           on_message=central_system_message,
                           on_close=central_system_link_down)
    log.setup(LOGLEVEL, LOGFILE)

    if not SOAP.start():
        log.error('APP:SOAP service error. Please check settings')
        sys.exit()
    if not WS.start():
        log.error('APP:Websocket service error. Please check settings')
        sys.exit()

    task.LoopingCall(lambda: vacuum(TIMEOUT)).start(VACUUM_TIMEOUT)

    reactor.run()
