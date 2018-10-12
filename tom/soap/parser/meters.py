from tom.soap.parser import helpers as xml


def parse(body):
    """ прочитать MeterValues"""
    return _parse_node(body)


def _parse_node(root):
    """ проичитать один узел """
    result = dict()
    result['values'] = []
    for node in root:
        name = xml.get_element_localname(node)
        if len(node):
            if name == 'values':
                result['values'].append(_parse_values(node))
            else:
                data = _parse_node(node)
        else:
            result[name] = node.text
    return result


def _parse_values(root):
    """ прочитать узел с измерениями """
    result = dict()
    result['values'] = []
    for node in root:
        name = xml.get_element_localname(node)
        if(name == 'timestamp'):
            result['timestamp'] = node.text
        elif (name == 'value'):
            result['values'].append(_parse_value(node))
    return result


def _parse_value(root):
    """ прочитать одно измерение """
    result = dict()
    result['value'] = root.text
    result.update(root.attrib)
    return result
