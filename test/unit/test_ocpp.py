""" Tests for SOAP parser"""
import unittest
import tom.ocpp.message as message
import tom.ocpp.error as error


class OCPPTest(unittest.TestCase):
    """ Base ocpp message tests """

    def test_error_default(self):
        err = error.create()
        self.assertEqual(err['Type'], message.ERROR)
        self.assertEqual(err['MessageID'], None)
        self.assertEqual(err['Payload']['ErrorCode'], 'GenericError')
        self.assertEqual(err['Payload']['ErrorDescription'], None)

    def test_error_default(self):
        err = error.create('232', 'SuperError')
        self.assertEqual(err['Type'], message.ERROR)
        self.assertEqual(err['MessageID'], '232')
        self.assertEqual(err['Payload']['ErrorCode'], 'GenericError')
        self.assertEqual(err['Payload']['ErrorDescription'], 'SuperError')
