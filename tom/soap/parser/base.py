"""
SOAP Parser
"""
from io import BytesIO
from lxml import etree

from tom.ocpp import message
from tom.soap.parser.header import parse as parse_header
from tom.soap.parser.body import parse as parse_body


def parse(data):
    """ Разобрать SOAP-сообщение и представить в виде OCPP-сообщения
    data - входные данные. Формат - байты
    Возвращает сообщение OCPP
    """
    try:
        root = etree.parse(BytesIO(data))
        header = parse_header(root)
        body = parse_body(root)
        return {**header, **body}
    except:
        pass
    return message.create()
