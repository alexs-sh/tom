""" Немного полезных функий """
import time


def now():
    """ Текущее время """
    return time.time()


def duration(begin, end):
    """ Абс. разница между 2-мя величинами """
    return abs(end - begin)
