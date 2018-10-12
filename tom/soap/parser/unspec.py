""" Default parser.
    Builds message through recursive descent.
"""
from typing import List
from tom.soap.parser import helpers as xml


def parse(body):
    """ Обычное чтение тела сообщения.
    Обычное - значит, что мы можем применить рекурсивный спуск для всех узлов.
    """
    return _parse_node(body)


def _insert_or_append(dst, src):
    """ добавить новые пары ключ-значения к уже разобранным """
    # Добавление нового значения в словарь. При этом:
    # выполняется нормализация значения
    # если значение встречается больше одного раза, то оно добавляется в массив
    # k - ключ в добавляемом словаре
    # v - добавляемое значение
    # e - существующее значение
    for (k, v) in src.items():
        if(v is None):
            continue
        if(k in dst.keys()):
            e = dst[k]
            if isinstance(e, List):
                dst[k].append(v)
            else:
                dst[k] = [e, v]
        else:
            dst[k] = v


def _parse_node(root):
    """ проичитать один узел """
    result = dict()
    for node in root:
        name = xml.get_element_localname(node)
        if len(node):
            data = _parse_node(node)
        else:
            data = node.text
        _insert_or_append(result, {name: data})
    return result
