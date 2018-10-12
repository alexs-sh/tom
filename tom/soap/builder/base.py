import uuid
from lxml import etree
from tom.soap import namespace as ns
from tom.ocpp import message
from tom.ocpp import error


def _header_action(msg_type, action):
    """ Перевести имя операции из OCPP в SOAP-Header """
    if msg_type == message.CALL:
        return '/' + action + 'Request'
    elif msg_type == message.RESULT:
        return '/' + action + 'Response'
    # TODO: add ERROR


def _body_action(msg_type, action):
    """ Перевести имя операции из OCPP в SOAP-Body """
    if msg_type == message.CALL:
        return action[0].lower() + action[1:] + 'Request'
    if msg_type == message.RESULT:
        return action[0].lower() + action[1:] + 'Response'
    # TODO: add ERROR


def _body_namespace(action):
    """ Определить namespace исходя из имени операции """
    cs = [
        'Authorize',
        'StartTransaction',
        'StopTransaction',
        'Heartbeat',
        'MeterValues',
        'BootNotification',
        'StatusNotification',
        'FirmwareStatusNotification',
        'DiagnosticsStatusNotification',
        'DataTransfer']

    if action in cs:
        return ns.CENTRAL_SYSTEM
    return ns.CHARGE_POINT


def _with_ns(element, namespace):
    """ Добавить namespace к имени"""
    if(namespace is None):
        return element
    return '{' + namespace + '}' + element


def _build_header(msg, downward):
    """ Постролить заголовок SOAP-сообщения. Header """
    NSMAP = {'soap': ns.SOAP_ENVELOPE, 'cp': ns.CHARGE_POINT,
             'cs': ns.CENTRAL_SYSTEM, 'wsa5': ns.ADDRESSING}
    msg_type = msg['Type']
    action = msg['Action']

    envelope = etree.Element(
        _with_ns('Envelope', ns.SOAP_ENVELOPE), nsmap=NSMAP)
    header = etree.SubElement(envelope, _with_ns('Header', ns.SOAP_ENVELOPE))

    act = etree.SubElement(header, _with_ns('Action', ns.ADDRESSING))
    act.text = '/' + action

    # Добавление опциональных параметров
    try:
        msg_id = msg['MessageID']
    except:
        msg_id = str(uuid.uuid4())

    element = etree.SubElement(header, _with_ns('MessageID', ns.ADDRESSING))
    element.text = 'urn:uuid:' + msg_id

    try:
        name = 'To'
        record = msg[name]
        if record != '':
            element = etree.SubElement(header, _with_ns(name, ns.ADDRESSING))
            element.text = msg[name]
    except:
        to = etree.SubElement(header, _with_ns('To', ns.ADDRESSING))
        to.text = 'http://www.w3.org/2005/08/addressing/anonymous'

    try:
        name = 'RelatesTo'
        record = msg[name]
        if record != '':
            element = etree.SubElement(header, _with_ns(name, ns.ADDRESSING))
            element.text = 'urn:uuid:' + msg[name]
    except:
        pass

    try:
        name = 'chargeBoxIdentity'
        record = msg[name]
        nspace = ns.CHARGE_POINT if downward else ns.CENTRAL_SYSTEM
        if record != '':
            element = etree.SubElement(
                header, _with_ns(name, nspace))
            element.text = record
    except:
        pass

    try:
        name = 'From'
        record = msg[name]
        if record != '':
            frm = etree.SubElement(header, _with_ns(name, ns.ADDRESSING))
            addr = etree.SubElement(frm, _with_ns('Address', ns.ADDRESSING))
            addr.text = record
    except:
        pass

    try:
        name = 'ReplyTo'
        record = msg[name]
        if record == '':
            record = 'http://www.w3.org/2005/08/addressing/anonymous'
        frm = etree.SubElement(header, _with_ns(name, ns.ADDRESSING))
        addr = etree.SubElement(frm, _with_ns('Address', ns.ADDRESSING))
        addr.text = record
    except:
        pass

    body = etree.SubElement(envelope, _with_ns('Body', ns.SOAP_ENVELOPE))
    body_ns = _body_namespace(action)
    body_act = _body_action(msg_type, action)
    payload = etree.SubElement(body, body_act)
    payload.attrib['xmlns'] = body_ns
    if msg['Payload'] != '':
        _build_body(payload, msg['Payload'])
    return envelope


def _build_body(root, msg):
    """ Посторить тело сообщения. BODY"""
    for (k, v) in msg.items():
        el = etree.SubElement(root, k)
        if hasattr(v, 'items'):
            _build_body(el, v)
        else:
            el.text = str(v)


def build(msg, downward=False):
    """ Собрать SOAP Envelope из OCPP сообщения.
    msg - сообщение
    downward - направление. True - восходящее (от ЗС к ЦС). В противном случае от ЦС к ЗС
    """
    try:
        root = _build_header(msg, downward)
        return etree.tostring(root)

    except:
        return ''
