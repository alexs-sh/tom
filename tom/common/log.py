"""
    Логгирование
"""
import logging


def instance():
    """ Получить экземпляр логгера """
    return logging.getLogger('log')


def _level(level):
    """ перевести строку с уровнем в понятную для logging'а форму """
    level = level.lower()
    table = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING,
             'error': logging.ERROR}

    try:
        return table[level]
    except:
        return logging.ERROR


def setup(level='error', file=None):
    """ Инициализация """
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('log')
    logger.setLevel(_level(level))

    # Логгирование в stdout
    stdout = logging.StreamHandler()
    stdout.setLevel(_level(level))
    stdout.setFormatter(formatter)
    logger.addHandler(stdout)

    # Логгирование в файл
    if file is not None:
        file = logging.FileHandler(file)
        file.setLevel(_level(level))
        file.setFormatter(formatter)
        logger.addHandler(file)


def debug(msg, *args, **kwargs):
    """
    Записать отпладочно сообщение
    """
    instance().debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """
    Записать информационное сообщение
    """
    instance().info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """
    Записать предупреждение
    """
    instance().warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """
    Записать ошибку
    """
    instance().error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    """
    Записать крит. ошибку
    """
    instance().critical(msg, *args, **kwargs)
