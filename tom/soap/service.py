from twisted.internet import reactor
from twisted.internet import task
from tom.soap.server import base as server
from tom.soap.client import pool
from tom.ocpp import message
from tom.common.utils import now, duration


class Service:
    """
    SOAP - сервис. Объединяет в себе SOAP-сервер и пул клиентов SOAP.
    """

    def __init__(self, port, on_message, on_expire, interface='0.0.0.0', inactive_timeout=10):
        self._server = server.Server(interface=interface,
                                     port=port,
                                     on_message=self._on_message)
        self._clients = pool.Pool(self._on_message)
        self._user_on_message = on_message
        self._user_on_expire = on_expire
        self._timestamps = dict()
        self._timeout = inactive_timeout

    def start(self):
        """ Запуск """
        inactive = task.LoopingCall(self._on_inactive_check)
        inactive.start(5)
        return self._server.start()

    def send(self, charge, msg):
        """ Отправка сообщения к ЗС """
        return self._clients.send(charge, msg)

    def _on_message(self, charge, msg, sender):
        """ Обработчик входящих сообщений от ЗС"""

        msg_type = msg['Type']
        if msg_type == message.CALL:
            address = msg['From']
            self._clients.link(charge, address)

        if msg_type in (message.CALL, message.RESULT):
            self._timestamps[charge] = now()

        return self._user_on_message(charge, msg, sender)

    def _on_inactive_check(self):
        """ Проверка таймаутов ЗС """
        expired = []
        current = now()
        for (k, v) in self._timestamps.items():
            if duration(current, v) >= self._timeout:
                expired.append(k)

        for charge in expired:
            self._clients.unlink(charge)
            del self._timestamps[charge]
            self._user_on_expire(charge)
