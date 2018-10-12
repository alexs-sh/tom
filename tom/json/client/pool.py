import json
from twisted.internet import reactor
from io import StringIO
from tom.common import log
from tom.ocpp import message
from tom.json.client.base import Connection, Status


class Client:
    MESSAGE_LIMIT = 8

    def __init__(self, charge, url, on_open, on_message, on_close):
        """
        Создать клиента
        charge - имя зарядной станции, для которой создано подключение
        url - адрес для подключения [ws//ip:port/ext]
        on_message - функция для уведомления о поступлении нового сообщения
        """
        self._charge = charge
        self._user_on_close = on_close
        self._user_on_message = on_message
        self._user_on_open = on_open
        self._url = url
        self._connection = Connection()

    def send(self, msg, make_connection):
        """
        Отправить сообщение
        msg - сообщение (байты)
        make_connection - разрешить создание подключения если оно не установлено.
        """
        log.debug('WS client:[{0}] try to send {1}: '.format(
            self._charge, msg))

        status = self._connection.status

        # Подключения нет и его создание запрещено -> отправка в принципе невозможна
        if make_connection is False and status != Status.CONNECTED:
            return False

        if status == Status.DISCONNECTED:
            # Подключение отсутсвует. Подключаем, сохранив сообщение в очереди
            address = '{0}/{1}'.format(self._url, self._charge)
            res = Connection.create(
                address, self._on_open, self._on_message, self._on_close)
            if res is True:
                self._connection = Connection(Status.CONNECTING)
            log.info(
                'WS client:[{0}] start connecting to {1} with result {2}'.format(self._charge, address, res))

        elif status == Status.CONNECTING:
            log.info(
                'WS client:[{0}] connection in progress'.format(self._charge))

        elif status == Status.CONNECTED:
            # Подключение установлено. Передаем сообщение получателю
            res = self._connection.send(msg)
            log.info('WS client:[{0}] message sent with result {1}'.format(
                self._charge, res))

    def close(self):
        """ Закрыть клиента """
        self._connection.close()
        self._connection = Connection(Status.DISCONNECTED)

    @property
    def charge(self):
        """ Вернуть имя станиции, с которым связан клиент"""
        return self._charge

    def _on_close(self):
        """ Обработчик закрытия. Вызывается при закрытии коннекта со стороны сервера, либо при неудачном подключении """
        log.info('WS client:[{0}] connection closed'.format(self._charge))
        self._connection = Connection(Status.DISCONNECTED)
        self._user_on_close(self._charge)

    def _on_open(self, connection):
        """ Обработчик успешного подключение """
        log.info(
            'WS client:[{0}] connection established'.format(self._charge))
        # Сохранить коннект
        self._connection = connection

        # Сбросить сообщения
        self._user_on_open(self._charge)

    def _on_message(self, payload):
        """ Обработчик входящего сообщения """
        log.debug('WS client:[{0}] receive {1}'.format(self._charge, payload))
        log.info('WS client:[{0}] receive message'.format(self._charge))

        # Передать в обработку на верх
        self._user_on_message(self, payload)


class Pool:

    """
    Пул клинетов WS
    Служит для упрощения взаимодействяи со множеством клиентов
    """

    def __init__(self, url,  on_open, on_message, on_close):
        self._clients = dict()
        self._url = url
        self._user_on_open = on_open
        self._user_on_message = on_message
        self._user_on_close = on_close

    def send(self, charge, msg, make_connection):
        """
        Отправить сообщение от станции
        """
        try:
            if charge in self._clients:
                client = self._clients[charge]
            else:
                client = Client(charge=charge,
                                url=self._url,
                                on_open=self._on_open,
                                on_message=self._on_message,
                                on_close=self._on_close)
                self._clients[charge] = client

            request = _make_json(msg)
            client.send(request, make_connection)
        except Exception as e:
            log.error(
                'WS pool:[{0}] send failed. Error description {1} '.format(charge, e))

    def drop(self, charge):
        """
        Закрыть клиента
        """
        try:
            client = self._clients[charge]
            client.close()
            return True
        except:
            pass
        return False

    def _on_open(self, charge):
        """ Подключение установлено """
        self._user_on_open(charge)

    def _on_close(self, charge):
        """ Подключение закрыто """
        self._user_on_close(charge)

    def _on_message(self, client, payload):
        """
        Получено сообщения от ЦС
        client - клиент (Client), получивший сообщение
        payload - сообщение (байты)
        Задача метода:
            обработать входящее сообщение
            создать функцию для отправки ответа, завернув в неё все необходимое
            передать на верх сообщения и функцию
        """

        # Прочитать сообщение
        msg = _make_ocpp(payload)
        if msg is None:
            return

        # Если это вызов (CALL), создать функтор для отпарвки ответа
        if msg['Type'] == message.CALL:
            def sender(response): return client.send(_make_json(response))
        else:
            sender = None

        # Передать на верх
        msg['chargeBoxIdentity'] = client.charge
        self._user_on_message(client.charge, msg, sender)


def _make_json(msg):
    """ JSON (байты) из OCPP сообщения """
    msg_type = msg['Type']
    if msg_type == message.CALL:
        result = [msg_type, msg['MessageID'], msg['Action'], msg['Payload']]
    elif msg_type == message.RESULT:
        result = [msg_type, msg['MessageID'], msg['Payload']]
    elif msg_type == message.ERROR:
        code = msg['Payload']['ErrorCode']
        try:
            descr = msg['Payload']['ErrorDescription']
            result = [msg_type, msg['MessageID'], code, descr]
        except:
            result = [msg_type, msg['MessageID'], code]

    return json.dumps(result).encode()


def _make_ocpp(data):
    """ OCPP сообщение из JSON (байты)"""
    try:
        data = data.decode('utf8')
        data = json.load(StringIO(data))
        msg = message.create()
        msg_type = data[0]
        msg['Type'] = msg_type
        msg['MessageID'] = data[1]
        if msg_type == message.CALL:
            msg['Action'] = data[2]
            msg['Payload'] = data[3]
        elif msg_type == message.RESULT:
            msg['Payload'] = data[2]
        elif msg_type == message.ERROR:
            msg['Payload'] = data[2]
        else:
            return None

        return msg

    except:
        pass
    return None
