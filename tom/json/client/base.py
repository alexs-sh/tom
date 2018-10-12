from enum import Enum
from autobahn.websocket.util import parse_url
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


class Status(Enum):
    """
    Состояния подключения
    """
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2


class Connection(WebSocketClientProtocol):

    """ Клиент WS
    Реализует поведение и передачу событий от twisted к клиентсокму коду (через ClientData)
    """

    def __init__(self, status=Status.DISCONNECTED):
        super().__init__()
        self._status = status

    def onOpen(self):
        """
        Обработчик завершения подключения
        """
        self._status = Status.CONNECTED
        self.factory.on_open(self)
        self.factory.connection_made = True

    def onMessage(self, payload, isBinary):
        """
        Обработчик для входящий сообщений
        """
        self.factory.on_message(payload)

    def onClose(self, wasClean, code, reason):
        """
        Обработчик обрыва подключения
        Будет вызван только если подключение было успешно установлено
        """
        self._status = Status.DISCONNECTED
        self.factory.on_close()

    def send(self, msg):
        """
        Отправить сообщение
        msg - массим байтов
        return - True в случае успеха
        """
        try:
            if self._status == Status.CONNECTED:
                self.sendMessage(msg)
                return True
        except:
            pass
        return False

    def close(self):
        """
        Закрыть подключение
        """
        try:
            # Коннект может быть неподключенным. Тогда получим исключение
            self.sendClose()
        except:
            pass

        self._status = Status.DISCONNECTED

    @property
    def status(self):
        """ Состояние коннекта """
        return self._status

    @staticmethod
    def create(url, on_open, on_message, on_close):
        """ Создать подключение """
        try:
            parsed = parse_url(url)

            ip = parsed[1]
            port = parsed[2]

            factory = ClientFactory(url, on_open, on_message, on_close)
            reactor.connectTCP(ip, port, factory, timeout=5)
            return True
        except:
            pass
        return False


class ClientFactory(WebSocketClientFactory):
    """ Факта для создания новый WS подключений.
    Основная задча - передать ряд параметров из вызывающего кода в эксземпляр класса-подключения.
    Так же позволяет ускорить реакцию на проблемы с подключением, путем переопределения stopFactory
    """

    def __init__(self, url, on_open, on_message, on_close):
        super().__init__(u'{0}'.format(url), protocols=['ocpp1.5'])
        self.protocol = Connection
        self.on_open = on_open
        self.on_message = on_message
        self.on_close = on_close
        self.connection_made = False

    def stopFactory(self):
        super().stopFactory()
        if self.connection_made is False:
            self.on_close()
