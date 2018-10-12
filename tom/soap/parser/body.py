""" SOAP body's parser
"""
from tom.ocpp import message
from tom.soap.parser import helpers as xml
from tom.soap.parser.unspec import parse as parse_unspec
from tom.soap.parser.meters import parse as parse_meters


def parse(root):
    """ Parse SOAP body """
    body = xml.get_element(root, 'Body')
    body = body[0]
    action = xml.get_element_localname(body)
    parser = _get_parser(action)
    payload = parser(body)
    _normalize(payload)
    return {'Type': _get_message_type(action), 'Payload': payload}


def _get_message_type(name):
    """ Определить тип сообщения """
    if name is not None:
        if name.find('Response') != -1:
            return message.RESULT
        if name.find('Request') != -1:
            return message.CALL
    return ''


def _get_parser(action):
    """ вернуть спец. парсер для особых сообщений """
    registry = {'meterValuesRequest': parse_meters}
    return registry[action] if action in registry else parse_unspec


def _normalize(payload):
    """ Нормализация значений. Конвератция из текста в нормальные типы если это возможно/необходимо """
    ignore = ['chargePointSerialNumber', 'imsi', 'iccid', 'firmwareVersion', 'idTag',
              'messageId', 'vendorId', 'vendorErrorCode', 'value']

    special = {'transactionId': _fix_transaction_id}
    for key in payload.keys():
        value = payload[key]

        # Значение этого параметра остается как есть
        if key in ignore:
            continue

        # Значение этого параметра требует особой обработки
        if key in special:
            payload[key] = special[key](value)
            continue

        # Если значение = строка, то пробуем сконвертировать его во float/int
        try:
            payload[key] = float(value) if '.' in value else int(value)
            continue
        except Exception:
            pass

        # Если значение не простой тип, то рекурсивно нормализуем его
        try:
            _normalize(value)
            continue
        except Exception:
            pass


def _fix_transaction_id(value):
    """ Исправить номер транзакции"""
    if value is None:
        return 0
    try:
        value = int(value)
    except:
        return 0
    return value
