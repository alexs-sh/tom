from zope.interface import implementer
from twisted.internet import reactor
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
from twisted.internet.defer import succeed
from tom.soap.parser import base as parser
from tom.soap.builder import base as builder
from tom.common import log
from tom.ocpp import message
from tom.ocpp import error


class Addresses:
    def __init__(self):
        self._addresses = dict()

    def get(self, charge):
        try:
            return self._addresses[charge]
        except:
            return None

    def add(self, charge, address):
        self._addresses[charge] = address

    def rem(self, charge):
        try:
            del self._addresses[charge]
        except:
            pass


@implementer(IBodyProducer)
class BytesProducer(object):
    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):

        pass


class Pool:
    def __init__(self, on_message):
        self._addresses = Addresses()
        self._on_message = on_message

    def link(self, charge, address):
        self._addresses.add(charge, address)

    def unlink(self, charge):
        self._addresses.rem(charge)

    def send(self, charge, msg):
        address = self._addresses.get(charge)

        if address is None:
            return False

        msg['To'] = address
        res = builder.build(msg, True)
        action = '/' + msg['Action']
        agent = Agent(reactor)
        request = agent.request(
            b'POST',
            bytes(address, 'utf-8'),
            Headers({'Content-type': ['application/soap+xml; charset=UTF-8; action="{0}"'.format(action)],
                     'Accept': ['*/*'], 'Connection': ['close']}), BytesProducer(res))

        def on_error(info): return self._on_error(info, msg)

        def on_response(response): return self._on_response(response, msg)

        request.addErrback(on_error)
        request.addCallback(on_response)

        log.info('SOAP client:[{0}] send message'.format(charge))
        log.debug('SOAP client:[{0}] send {1}'.format(charge, res))

        return True

    def _on_error(self, info, request):
        """
        Обработчик ошибки
        info - информация об ошибке
        request - обрабатываемый запрос
        """
        try:
            charge = request['chargeBoxIdentity']
            msg_id = request['MessageID']
            response = error.create(msg_id, 'NotRespond')
            response['RelatesTo'] = msg_id
            self._on_message(charge, response, None)
        except:
            pass
        log.error('SOAP client:[{0}] error {1}'.format(
            charge, info.getErrorMessage()))

    def _on_response(self, response, request):
        """
        Обработчик ответа.
        response - HTTP ответ
        request - обрабатываемый запрос
        Обработка ответа выполняется в 2 этапа:
            чтения HTTP-заголовка
            чтение тела сообщения
        """
        if response is None:
            return

        code = response.code
        body = readBody(response)

        # Прочитать тело сообщения
        def on_read(body): return self._on_body(body, code, request)
        body.addCallback(on_read)

        return body

    def _on_body(self, body, code, request):
        """
        Обработчик чтения тела сообщения
        body - тело сообщения (байты)
        code - HTTP - code
        request - обрабатываемый запрос
        """

        log.info('SOAP client: receive message')
        log.debug('SOAP client: receive {0}'.format(body))

        SUCCESS_CODE = 200
        charge = request['chargeBoxIdentity']
        response = parser.parse(body)
        valid_response = message.validate(response)
        valid_code = code == SUCCESS_CODE
        if valid_response and valid_code:
            self._on_message(charge, response, None)
        else:
            charge = request['chargeBoxIdentity']
            msg_id = request['MessageID']
            response = error.create(msg_id, 'NotRespond')
            response['RelatesTo'] = msg_id
            self._on_message(charge, response, None)
            log.error('SOAP:[{0}] invalid message (code = {1} validate={2}) {3}'.format(
                charge, code, valid_response, body))


...
