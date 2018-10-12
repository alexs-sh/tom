""" SOAP header's parser """
from tom.ocpp import message
from tom.soap.parser import helpers as xml


def parse(root):
    """
    Прочитать заголовок из SOAP-сообщения
    root - родительский узел
    """
    msg = message.create()
    header = xml.get_element(root, 'Header')
    msg['chargeBoxIdentity'] = xml.get_element_text(
        header, 'chargeBoxIdentity')
    msg['From'] = xml.get_element_text(
        xml.get_element(header, 'From'), 'Address')
    msg['To'] = xml.get_element_text(header, 'To')
    msg['ReplyTo'] = xml.get_element_text(
        xml.get_element(header, 'ReplyTo'), 'Address')
    msgid = xml.get_element_text(header, 'MessageID')
    relates = xml.get_element_text(header, 'RelatesTo')
    action = xml.get_element_text(header, 'Action')
    msg['MessageID'] = _fix_message_id(msgid)
    msg['RelatesTo'] = _fix_message_id(relates)
    msg['Action'] = _fix_action(action)
    return msg


def _fix_action(action):
    """ Удалить слэши и др. Request/Response из имени опреации """
    if action is None:
        return ''

    fixed = action
    if fixed[0] == '/':
        fixed = fixed[1:]

    type_pos = fixed.find('Request')
    if type_pos != -1:
        return fixed[:type_pos]

    type_pos = fixed.find('Response')
    if type_pos != -1:
        return fixed[:type_pos]

    return fixed


def _fix_message_id(msgid):
    """ Убрать namespace из MessageID """
    if msgid is None:
        return ''

    pos = msgid.find(':')
    if pos != -1:
        return _fix_message_id(msgid[pos + 1:])
    return msgid
