from autobahn.websocket.util import parse_url
from tom.common import log
from tom.json.client import pool


class Service:
    """ WS сервис """

    def __init__(self, url, on_open, on_message, on_close):
        """
        url - адрес для подключения ws://ip:port/ext
        on_message - обработчик входящих сообщений. Функция с 3 аргументами: имя ЗС, сообщение, функция для отправки ответа (ОПЦ)
        """
        self._clients = pool.Pool(url=url,
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_close=on_close)
        self._url = url

    def start(self):
        """
        Запустить
        Возвращает True в случае успеха
        """
        try:
            parse_url(self._url)
            return True
        except:
            pass
        return False

    def send(self, charge, msg, make_connection=False):
        """ Отправить сообщения в ЦС
        charge - имя ЗС
        msg - сообщение
        make_connection - рузрашеить создание подключения, если оно не существует
        """
        self._clients.send(charge, msg, make_connection)

    def drop(self, charge):
        """
        Закрыть подключение связанное с ЗС
        charge - имя ЗС
        """
        self._clients.drop(charge)
