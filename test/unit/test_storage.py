import unittest
import time
from tom.storage.base import MessageStorage
from tom.common.utils import now, duration


class Counter:
    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1


def limited_selector(record, counter, limit):
    if counter.value < limit:
        counter.inc()
        return True
    else:
        return None


def timed_selector(record, timeout):

    if duration(now(), record.timestamp) >= timeout:
        return True
    return False


def charge_selector(record, charge):

    if record.message['chargeBoxIdentity'] == charge:
        return True
    return False


def all_selector(record):
    return True


class StorageTest(unittest.TestCase):
    """ Base storage's tests """

    def test_count(self):
        limit = 1000
        s = MessageStorage()
        for i in range(0, limit):
            s.add(i, i, None)

        self.assertEqual(limit, s.count())

    def test_empty_done(self):
        s = MessageStorage()
        s.add(1, 1, None)
        s.done(1, None)
        self.assertEqual(s.count(), 0)

    def test_done(self):
        s = MessageStorage()
        cnt = Counter()

        def on_done(x): return x.inc()
        s.add(1, 1, on_done)
        s.done(1, cnt)
        self.assertEqual(cnt.value, 1)
        self.assertEqual(s.count(), 0)

    def test_add_limit(self):
        limit = MessageStorage.MAX_SIZE + 100
        s = MessageStorage()
        for i in range(0, limit):
            res = s.add(i, i, None)
            if i > MessageStorage.MAX_SIZE:
                self.assertEqual(res, False)

        self.assertEqual(s.count(), MessageStorage.MAX_SIZE)

    def test_select(self):
        limit = 1000
        offset = 2000
        s = MessageStorage()
        for i in range(0, limit):
            msg = {'chargeBoxIdentity': 'NoSelect', 'value': i}
            s.add(i, msg, None)

            msg = {'chargeBoxIdentity': 'Select', 'value': i + offset}
            s.add(i + offset, msg, None)

        self.assertEqual(s.count(), limit * 2)

        def select(x): return charge_selector(x, 'Select')
        res = s.select(select)

        self.assertEqual(len(res), limit)

        for r in res:
            v = r['value']
            cmp = v >= offset and v <= offset + limit
            self.assertTrue(cmp)

    def test_limited(self):
        limit = 1000
        s = MessageStorage()
        cnt = Counter()

        def select(x): return limited_selector(x, cnt, 400)
        for i in range(0, limit):
            s.add(i, i, None)

        s.vacuum(select)
        self.assertEqual(s.count(), 600)

    def test_autoclean_time(self):
        limit = 1000
        s = MessageStorage()
        for i in range(0, limit):
            s.add(i, i, None)
        time.sleep(1)
        self.assertEqual(s.count(), limit)

        def select(x): return timed_selector(x, 0.5)
        s.vacuum(select)
        self.assertEqual(s.count(), 0)

    def test_clean_charge(self):
        limit = 1000
        offset = 2000
        s = MessageStorage()
        for i in range(0, limit):
            msg = {'chargeBoxIdentity': 'NoDelete', 'value': i}
            s.add(i, msg, None)

            msg = {'chargeBoxIdentity': 'Delete', 'value': i + offset}
            s.add(i + offset, msg, None)

        self.assertEqual(s.count(), limit * 2)

        def select(x): return charge_selector(x, 'Delete')
        s.vacuum(select)

        self.assertEqual(s.count(), limit)

    def test_deleter(self):
        limit = 1000
        cnt = Counter()

        def deleter(x): return cnt.inc()
        s = MessageStorage(deleter=deleter)
        for i in range(0, limit):
            s.add(i, i, None)

        def select(x): return True
        s.vacuum(select)
        self.assertEqual(cnt.value, limit)

    def test_done2(self):
        limit = 1000
        s = MessageStorage()
        cnt = Counter()

        def on_done(x): return cnt.inc()
        for i in range(0, limit):
            s.add(i, i, on_done)

        for i in range(0, limit):
            s.done(i+20000, None)

        self.assertEqual(cnt.value, 0)
        self.assertEqual(s.count(), limit)
