import tom.ocpp.message as message


def create(id=None, description=None):
    """ Создать OCPP сообщение об ошибке """
    msg = message.create()
    msg['Type'] = message.ERROR
    msg['MessageID'] = id
    msg['Payload'] = dict()
    msg['Payload']['ErrorCode'] = 'GenericError'
    if description is not None:
        msg['Payload']['ErrorDescription'] = description

    return msg
