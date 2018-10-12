import sys
import tom.ocpp.message as message
import tom.soap.client.pool as pool
import uuid
from twisted.internet import reactor
from twisted.internet import task


class State:
    def __init__(self):
        self._state = 'connect'
        self._messages = dict()

    def is_connected(self):
        return self._state in ('boot')

    def connected(self):
        if self._state == 'connect':
            self._state = 'boot'

    def reset(self):
        self._state = 'connect'

    def add_message(self, msg_id):
        self._messages[msg_id] = True

    def check_and_remove_message(self, msg_id):
        result = msg_id in self._messages

        if result:
            del self._messages[msg_id]

        return result


def on_done(charge, response, sender):

    success = response['Type'] == message.RESULT

    if success:
        if not STATE.is_connected():
            STATE.connected()
        else:
            msg_id = response['RelatesTo']
            if not STATE.check_and_remove_message(msg_id):
                print("Got wrong message ID")
                print(response)
                sys.exit(1)
    else:
        STATE.reset()


def generator():
    data = {}

    if STATE.is_connected():
        msg = make_call('Heartbeat', data)
        POOL.send(NAME, msg)
        STATE.add_message(msg['MessageID'])


def make_call(action, data):
    msg = message.create()
    msg['Action'] = action
    msg['MessageID'] = str(uuid.uuid4())
    msg['From'] = 'http://localhost/'
    msg['ReplyTo'] = 'http://www.w3.org/2005/08/addressing/anonymous',
    msg['chargeBoxIdentity'] = NAME
    msg['To'] = ADDRESS
    msg['Type'] = message.CALL

    payload = dict()
    for (k, v) in data.items():
        payload[k] = v

    msg['Payload'] = payload
    return msg


def connector():
    data = {
        'chargePointVendor': 'Schneider Electric',
        'chargePointModel': 'EVlink Smart Wallbox',
        'chargePointSerialNumber': '3N170740564A1S1B7551700014',
        'chargeBoxSerialNumber': 'EVB1A22P4RI3N1712406002002503A057',
        'firmwareVersion': '3.2.0.12'
    }
    if not STATE.is_connected():
        msg = make_call('BootNotification', data)
        POOL.send(NAME, msg)


def usage():
    print("Usage")
    print('\tpython test/test_client.py --charge=TESTZZZ  --cycle=1 --address="http://127.0.0.1:8888/"')


def read_arguments():
    result = {'charge': 'TEST', 'address': 'http://127.0.0.1:8080', 'cycle': 1}
    try:
        for arg in sys.argv:
            if arg.find('--charge') >= 0:
                _, charge = arg.split("=")
                result['charge'] = charge
            elif arg.find('--address') >= 0:
                _, address = arg.split("=")
                result['address'] = address
            elif arg.find('--cycle') >= 0:
                _, cycle = arg.split("=")
                result['cycle'] = float(cycle)
    except:
        usage()
        sys.exit()

    return result


if __name__ == '__main__':

    ARGS = read_arguments()
    STATE = State()
    POOL = pool.Pool(on_done)
    POOL.link(ARGS['charge'], ARGS['address'])
    NAME = ARGS['charge']
    ADDRESS = ARGS['address']
    con = task.LoopingCall(connector)
    con.start(10)

    gen = task.LoopingCall(generator)
    gen.start(ARGS['cycle'])

    reactor.run()
