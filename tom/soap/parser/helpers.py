""" XML Helpers"""
from lxml.etree import QName
from tom.soap import namespace
"""
SOAP PARSER
"""
KNOWN_ELEMENTS = {
    'Header': [namespace.SOAP_ENVELOPE],
    'Body': [namespace.SOAP_ENVELOPE],
    'chargeBoxIdentity': [namespace.CENTRAL_SYSTEM, namespace.CHARGE_POINT],
    'MessageID': [namespace.ADDRESSING],
    'From': [namespace.ADDRESSING],
    'To': [namespace.ADDRESSING],
    'ReplyTo': [namespace.ADDRESSING],
    'RelatesTo': [namespace.ADDRESSING],
    'Address': [namespace.ADDRESSING],
    'Action': [namespace.ADDRESSING]
}


def _append_namespace(name, ns):
    return '{' + ns + '}' + name


def _get_namespaces(name):
    return KNOWN_ELEMENTS[name]


def get_element(root, name):
    if root is None:
        return None

    namespaces = _get_namespaces(name)

    for ns in namespaces:
        node = root.find(_append_namespace(name, ns))
        if node is not None:
            return node
    return None


def get_element_localname(element):
    try:
        return QName(element.tag).localname
    except:
        pass
    return None


def get_element_text(root, name):
    """ Get text from element in xmldoc. Adds namespace to known elements"""
    try:
        element = get_element(root, name)
        return element.text
    except:
        pass
    return None
