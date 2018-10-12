from tom.common.utils import now, duration


class Record:

    """ Сообщение + необходимая вспом. информация """

    def __init__(self, message, on_done):
        self.message = message
        self.timestamp = now()
        self.on_done = on_done


class Records:

    """ Массив записей c к некоторыми плюшками """

    def __init__(self):
        self._records = dict()

    def add(self, key, message, on_done):
        """ добавить """
        self._records[key] = Record(message, on_done)

    def rem(self, key):
        """ удалить """
        try:
            del self._records[key]
        except:
            pass

    def move(self, key):
        """ переместить """
        try:
            res = self._records[key]
            del self._records[key]
            return res
        except:
            return None

    def find(self, key):
        """ найти """
        try:
            return self._records[key]
        except:
            return None

    def items(self):
        """ вернуть все записи """
        return self._records.items()

    def count(self):
        """ размер """
        return len(self._records.items())


def _default_deleter(record):
    """ дефолтный 'удалятор'. Чтобы не использоват ьи не проверять на None """
    pass


class MessageStorage:

    """ Класс для хранения сообщений. Кроме хранения реализует поведение в виде вызова
    обработчиков завершения запроса + автоочистку"""

    MAX_SIZE = 4096  # лимит для числа сообщений в хранилище. У нас нет каких-то жестких ограничений по ресурсам. Пусть будет, в виде защиты от дурака

    def __init__(self, deleter=_default_deleter):
        self._records = Records()
        self._deleter = deleter

    def add(self, key, message, on_done):
        """ Добавление нового значения в очередь сообщений """

        if self._records.count() >= MessageStorage.MAX_SIZE:
            return False

        if self._records.find(key) is None:
            self._records.add(key, message, on_done)
            return True

        return False

    def done(self, key, response):
        """ Уведомить очередь, что обработка сообщения завершена """
        try:
            msg = self._records.move(key)
            msg.on_done(response)
        except:
            pass

    def count(self):
        """ кол-во записей в хранилище """
        return len(self._records.items())

    def select(self, selector):
        """
        Выбрать записи из БД
        selector - функция для выборки удаляемых значений. Если она возвращает True - то значение будет выбрано. Если
        None, выборка прекратится
        """
        selected = []
        for k, v in self._records.items():
            res = selector(v)

            if res is None:
                break
            elif res is True:
                selected.append(v.message)

        return selected

    def vacuum(self, selector):
        """
        Очистить БД.
        selector - функция для выборки удаляемых значений. Если она возвращает True - то значение будет удалено.
        Если None - очистка прекратится
        """
        clean = []
        for k, v in self._records.items():
            res = selector(v)

            if res is None:
                break
            elif res is True:
                clean.append(k)

        [self._remove_record(k) for k in clean]
        return len(clean)

    def _remove_record(self, key):
        """ Удаление записи из хранилища """
        try:
            msg = self._records.move(key)
            response = self._deleter(msg)
            msg.on_done(response)
        except:
            pass
