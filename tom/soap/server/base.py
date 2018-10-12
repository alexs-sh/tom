"""
SOAP Server
"""
import io
from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from tom.common import log
from tom.ocpp import message
from tom.soap.parser import base as parser
from tom.soap.builder import base as builder


def _send_answer(response, request):
    """
    Функция для отправки ответов в ЗС
    response - ответ [ocpp.message]
    request - начальный запрос, полученный в render_POST. Он же служит и для отправки результатов
    """
    try:
        if response is not None:
            if response['Type'] == message.RESULT:
                res = builder.build(response)
                request.setResponseCode(200)
                request.setHeader(
                    'content-type', "application/soap+xml; charset=UTF-8")
                request.write(res)
                log.info('SOAP server: send response')
                log.debug('SOAP server:[{0}] send {1}'.format(
                    response['chargeBoxIdentity'], res))

                request.finish()
                return

        request.setResponseCode(500)
        request.finish()
        log.warning('SOAP server: drop message [response type != CALLRESULT]')
    except Exception as e:
        log.error("SOAP server:{0}".format(e))
        pass


class Events(resource.Resource):
    """ Wrapper for server events """
    isLeaf = True

    def __init__(self, on_message):
        """ Конструтктор
        on_message - обработчик входящих соообщений. Функция, принимающая 3 аргумента: имя ЗС, сообщение, функция для отправки ответа (опционально)"""
        super().__init__()
        self._user_on_message = on_message

    def render_POST(self, request):
        """ Запрос от ЗС """
        try:

            payload = io.BufferedReader(request.content).read()
            log.info('SOAP server: receive message')
            log.debug('SOAP server: receive {0}'.format(payload))
            msg = parser.parse(payload)

            if message.validate(msg):
                charge = msg['chargeBoxIdentity']

                def action(response): return _send_answer(response, request)
                if self._user_on_message(charge, msg, action):
                    return server.NOT_DONE_YET
                else:
                    log.warning('SOAP server: drop message')
            else:
                log.error('SOAP: invalid message {0}'.format(payload))
        except Exception as e:
            log.error('SOAP: {0}'.format(e))

        return ''


class Server:
    """
    SOAP - сервер
    """

    def __init__(self,  port, on_message, interface='0.0.0.0'):
        """
        port - порт, который бдует слушать сервер
        interface - имя интерфейса для приема входящих подключений
        on_message - обработчик входящих соообщений. Функция, принимающая 3 аргумента: имя ЗС, сообщение, функция для отправки ответа (опционально)
        """
        self._events = Events(on_message)
        self._port = port
        self._iface = interface
        self._endpoint = None

    def start(self):
        """ Start server
        """
        try:
            factory = server.Site(self._events)
            self._endpoint = endpoints.TCP4ServerEndpoint(reactor,
                                                          interface=self._iface,
                                                          port=self._port)
            listener = self._endpoint.listen(factory)
            # Простая проверка на увспешность опреации без добавления колбеков. Если
            # аттрибут 'startReading' присутвует в результате вызова listen, то listen
            # прошел усешно
            success = hasattr(listener.result, 'startReading')
            if not success:
                log.error('SOAP: {0}'.format(listener))

            return success
        except:
            return False

    def stop(self):
        """ Stop server """
        pass
