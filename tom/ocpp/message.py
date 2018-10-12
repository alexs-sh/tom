import uuid

"""
Message types
"""

CALL = 2
RESULT = 3
ERROR = 4


def create():
    """
    Создать OCPP сообщение с дефолтными полями
    """
    return {'chargeBoxIdentity': '', 'MessageID': '', 'From': '',
            'ReplyTo': '', 'To': '', 'RelatesTo': '', 'Action': '', 'Type': '', 'Payload': ''}


def validate(msg):
    """
    Проверить сообщение. Проверка выполняется по заголовочным полям. Тело сообщения
    в данном случае не слишком актуально
    """
    try:
        correct_id = (msg['MessageID'] != '' or msg['RelatesTo'] != '')
        correct_type = msg['Type'] != ''
        return correct_id and correct_type
    except:
        pass
    return False
