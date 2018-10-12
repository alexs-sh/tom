""" Tests for SOAP parser"""
import unittest
import tom.soap.parser.base as parser
from tom.ocpp import message


class SOAPParserTest(unittest.TestCase):
    """ Base parser's tests """

    def test_header(self):
        """ Test header """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cs:chargeBoxIdentity>powerwolf1</cs:chargeBoxIdentity><wsa5:MessageID>urn:uuid:c9e52d5d-ac61-46dc-a197-12c052ecb5d1</wsa5:MessageID><wsa5:From><wsa5:Address>http://localhost:8080/</wsa5:Address></wsa5:From><wsa5:ReplyTo><wsa5:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa5:Address></wsa5:ReplyTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://10.151.12.18:8888/steve/services/CentralSystemService</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/BootNotification</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cs:bootNotificationRequest><cs:chargePointVendor>Schneider Electric</cs:chargePointVendor><cs:chargePointModel>EVlink Smart Wallbox</cs:chargePointModel><cs:chargePointSerialNumber>3N170740564A1S1B7551700014</cs:chargePointSerialNumber><cs:chargeBoxSerialNumber>EVB1A22P4RI3N1712406002002503A057</cs:chargeBoxSerialNumber><cs:firmwareVersion>3.2.0.12</cs:firmwareVersion></cs:bootNotificationRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'chargeBoxIdentity': 'powerwolf1',
            'MessageID': 'c9e52d5d-ac61-46dc-a197-12c052ecb5d1',
            'From': 'http://localhost:8080/',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://10.151.12.18:8888/steve/services/CentralSystemService',
            'Action': 'BootNotification'
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_header_validate(self):
        """ Test header """
        empty_header = ''
        invalid_header = '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cs:chargeBoxIdentity>powerwolf1</cs:chargeBoxIdentity><wsa5:MssageID>urn:uuid:c9e52d5d-ac61-46dc-a197-12c052ecb5d1</wsa5:MssageID><wsa5:From><wsa5:Address>http://localhost:8080/</wsa5:Address></wsa5:From><wsa5:ReplyTo><wsa5:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa5:Address></wsa5:ReplyTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://10.151.12.18:8888/steve/services/CentralSystemService</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/BootNotification</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cs:bootNotificationRequest><cs:chargePointVendor>Schneider Electric</cs:chargePointVendor><cs:chargePointModel>EVlink Smart Wallbox</cs:chargePointModel><cs:chargePointSerialNumber>3N170740564A1S1B7551700014</cs:chargePointSerialNumber><cs:chargeBoxSerialNumber>EVB1A22P4RI3N1712406002002503A057</cs:chargeBoxSerialNumber><cs:firmwareVersion>3.2.0.12</cs:firmwareVersion></cs:bootNotificationRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        msg = parser.parse(empty_header)
        self.assertFalse(message.validate(msg))
        msg = parser.parse(invalid_header)
        self.assertFalse(message.validate(msg))

    def test_boot_notification_req(self):
        """ Test BootNotificationRequest """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cs:chargeBoxIdentity>powerwolf1</cs:chargeBoxIdentity><wsa5:MessageID>urn:uuid:c9e52d5d-ac61-46dc-a197-12c052ecb5d1</wsa5:MessageID><wsa5:From><wsa5:Address>http://localhost:8080/</wsa5:Address></wsa5:From><wsa5:ReplyTo><wsa5:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa5:Address></wsa5:ReplyTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://10.151.12.18:8888/steve/services/CentralSystemService</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/BootNotification</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cs:bootNotificationRequest><cs:chargePointVendor>Schneider Electric</cs:chargePointVendor><cs:chargePointModel>EVlink Smart Wallbox</cs:chargePointModel><cs:chargePointSerialNumber>3N170740564A1S1B7551700014</cs:chargePointSerialNumber><cs:chargeBoxSerialNumber>EVB1A22P4RI3N1712406002002503A057</cs:chargeBoxSerialNumber><cs:firmwareVersion>3.2.0.12</cs:firmwareVersion></cs:bootNotificationRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'chargeBoxIdentity': 'powerwolf1',
            'MessageID': 'c9e52d5d-ac61-46dc-a197-12c052ecb5d1',
            'From': 'http://localhost:8080/',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://10.151.12.18:8888/steve/services/CentralSystemService',
            'Type': message.CALL,
            'Action': 'BootNotification',
            'Payload': {
                'chargePointVendor': 'Schneider Electric',
                'chargePointModel': 'EVlink Smart Wallbox',
                'chargePointSerialNumber': '3N170740564A1S1B7551700014',
                'chargeBoxSerialNumber': 'EVB1A22P4RI3N1712406002002503A057',
                'firmwareVersion': '3.2.0.12'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_boot_notification_res(self):
        """ Test BootNotificationResponse """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/BootNotificationResponse</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:97236048-7d4a-4198-8636-cf9065bbe913</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://www.w3.org/2005/08/addressing/anonymous</To><RelatesTo xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:c9e52d5d-ac61-46dc-a197-12c052ecb5d1</RelatesTo></soap:Header><soap:Body><bootNotificationResponse xmlns="urn://Ocpp/Cs/2012/06/"><status>Accepted</status><currentTime>2018-08-15T07:01:00.992Z</currentTime><heartbeatInterval>14400</heartbeatInterval></bootNotificationResponse></soap:Body></soap:Envelope>'
        control = {
            'MessageID': '97236048-7d4a-4198-8636-cf9065bbe913',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'Action': 'BootNotification',
            'RelatesTo': 'c9e52d5d-ac61-46dc-a197-12c052ecb5d1',
            'Type': message.RESULT,
            'Payload':
            {
                'status': 'Accepted',
                'currentTime': '2018-08-15T07:01:00.992Z',
                'heartbeatInterval': 14400
            }
        }

        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_authorize_req(self):
        """ Test AuthorizeRequest """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cs:chargeBoxIdentity>ABC</cs:chargeBoxIdentity><wsa5:MessageID>urn:uuid:965ccd90-5e83-4467-9f51-eed6125cf6aa</wsa5:MessageID><wsa5:From><wsa5:Address>http://192.168.0.102:8080/</wsa5:Address></wsa5:From><wsa5:ReplyTo><wsa5:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa5:Address></wsa5:ReplyTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://192.168.0.100:8080/steve/services/CentralSystemService</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/Authorize</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cs:authorizeRequest><cs:idTag>0700001B0BFA68</cs:idTag></cs:authorizeRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': '965ccd90-5e83-4467-9f51-eed6125cf6aa',
            'From': 'http://192.168.0.102:8080/',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.100:8080/steve/services/CentralSystemService',
            'Action': 'Authorize',
            'Type': message.CALL,
            'Payload':
            {
                'idTag':  '0700001B0BFA68'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_authorize_res(self):
        """ Test AuthorizeResponse """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/AuthorizeResponse</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:70834a51-2e3f-4424-af62-caada6a9a7e8</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://www.w3.org/2005/08/addressing/anonymous</To><RelatesTo xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:965ccd90-5e83-4467-9f51-eed6125cf6aa</RelatesTo></soap:Header><soap:Body><authorizeResponse xmlns="urn://Ocpp/Cs/2012/06/"><idTagInfo><status>Accepted</status><expiryDate>2018-12-10T15:14:00.000Z</expiryDate></idTagInfo></authorizeResponse></soap:Body></soap:Envelope>'
        control = {
            'MessageID': '70834a51-2e3f-4424-af62-caada6a9a7e8',
            'RelatesTo': '965ccd90-5e83-4467-9f51-eed6125cf6aa',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'Action': 'Authorize',
            'Type': message.RESULT,
            'Payload':
            {
                'idTagInfo': {'status': 'Accepted', 'expiryDate': '2018-12-10T15:14:00.000Z'}
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_status_notification_req(self):
        """ Test StatusNotificationRequest """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cs:chargeBoxIdentity>ABC</cs:chargeBoxIdentity><wsa5:MessageID>urn:uuid:a6fe232d-b29f-4b1c-b127-09752124d2b7</wsa5:MessageID><wsa5:From><wsa5:Address>http://192.168.0.102:8080/</wsa5:Address></wsa5:From><wsa5:ReplyTo><wsa5:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa5:Address></wsa5:ReplyTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://192.168.0.100:8080/steve/services/CentralSystemService</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/StatusNotification</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cs:statusNotificationRequest><cs:connectorId>1</cs:connectorId><cs:status>Occupied</cs:status><cs:errorCode>NoError</cs:errorCode><cs:timestamp>2018-09-10T11:06:28Z</cs:timestamp></cs:statusNotificationRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': 'a6fe232d-b29f-4b1c-b127-09752124d2b7',
            'From': 'http://192.168.0.102:8080/',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.100:8080/steve/services/CentralSystemService',
            'Type': message.CALL,
            'Action': 'StatusNotification',
            'Payload': {
                'connectorId': 1,
                'status': 'Occupied',
                'errorCode': 'NoError',
                'timestamp': '2018-09-10T11:06:28Z',
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_status_notification_res(self):
        """ Test StatusNotificationResponse """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/StatusNotificationResponse</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:39736d2b-551e-486e-a820-bed4c702bf9d</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://www.w3.org/2005/08/addressing/anonymous</To><RelatesTo xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:a6fe232d-b29f-4b1c-b127-09752124d2b7</RelatesTo></soap:Header><soap:Body><statusNotificationResponse xmlns="urn://Ocpp/Cs/2012/06/"/></soap:Body></soap:Envelope>'
        control = {
            'Action': 'StatusNotification',
            'MessageID': '39736d2b-551e-486e-a820-bed4c702bf9d',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': 'a6fe232d-b29f-4b1c-b127-09752124d2b7',
            'Type': message.RESULT,
            'Payload': {
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_start_transaction_req(self):
        """ Test StartTransactionRequest """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cs:chargeBoxIdentity>ABC</cs:chargeBoxIdentity><wsa5:MessageID>urn:uuid:7a408b9c-5cf6-4158-8efd-e6bd135b0f67</wsa5:MessageID><wsa5:From><wsa5:Address>http://192.168.0.102:8080/</wsa5:Address></wsa5:From><wsa5:ReplyTo><wsa5:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa5:Address></wsa5:ReplyTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://192.168.0.100:8080/steve/services/CentralSystemService</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/StartTransaction</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cs:startTransactionRequest><cs:connectorId>1</cs:connectorId><cs:idTag>0700001B0BFA68</cs:idTag><cs:timestamp>2018-09-10T11:07:34Z</cs:timestamp><cs:meterStart>0</cs:meterStart></cs:startTransactionRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': '7a408b9c-5cf6-4158-8efd-e6bd135b0f67',
            'From': 'http://192.168.0.102:8080/',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.100:8080/steve/services/CentralSystemService',
            'Type': message.CALL,
            'Action': 'StartTransaction',
            'Payload': {
                'connectorId': 1,
                'idTag': '0700001B0BFA68',
                'timestamp': '2018-09-10T11:07:34Z',
                'meterStart': 0
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_start_transaction_res(self):
        """ Test StatusNotificationRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/StartTransactionResponse</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:d74736b5-838f-4dca-b9af-34fb62f40290</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://www.w3.org/2005/08/addressing/anonymous</To><RelatesTo xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:7a408b9c-5cf6-4158-8efd-e6bd135b0f67</RelatesTo></soap:Header><soap:Body><startTransactionResponse xmlns="urn://Ocpp/Cs/2012/06/"><transactionId>13</transactionId><idTagInfo><status>Accepted</status><expiryDate>2018-12-10T15:14:00.000Z</expiryDate></idTagInfo></startTransactionResponse></soap:Body></soap:Envelope>'
        control = {
            'Action': 'StartTransaction',
            'MessageID': 'd74736b5-838f-4dca-b9af-34fb62f40290',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': '7a408b9c-5cf6-4158-8efd-e6bd135b0f67',
            'Type': message.RESULT,
            'Payload': {
                'transactionId': 13,
                'idTagInfo': {'status': 'Accepted', 'expiryDate': '2018-12-10T15:14:00.000Z'}
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_stop_transaction_req(self):
        """ Test StopTransactionRequest """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cs:chargeBoxIdentity>ABC</cs:chargeBoxIdentity><wsa5:MessageID>urn:uuid:509c8ce0-7e45-4c2d-920e-1ddcb7d39f21</wsa5:MessageID><wsa5:From><wsa5:Address>http://192.168.0.102:8080/</wsa5:Address></wsa5:From><wsa5:ReplyTo><wsa5:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa5:Address></wsa5:ReplyTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://192.168.0.100:8080/steve/services/CentralSystemService</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/StopTransaction</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cs:stopTransactionRequest><cs:transactionId>13</cs:transactionId><cs:timestamp>2018-09-10T11:09:12Z</cs:timestamp><cs:meterStop>0</cs:meterStop><cs:transactionData></cs:transactionData></cs:stopTransactionRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': '509c8ce0-7e45-4c2d-920e-1ddcb7d39f21',
            'From': 'http://192.168.0.102:8080/',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.100:8080/steve/services/CentralSystemService',
            'Type': message.CALL,
            'Action': 'StopTransaction',
            'Payload': {
                'transactionId': 13,
                'timestamp': '2018-09-10T11:09:12Z',
                'meterStop': 0
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_stop_transaction_res(self):
        """ Test StopNotificationRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/StopTransactionResponse</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:6c9ec1cd-74d1-49a9-82d2-10dc46a29642</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://www.w3.org/2005/08/addressing/anonymous</To><RelatesTo xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:509c8ce0-7e45-4c2d-920e-1ddcb7d39f21</RelatesTo></soap:Header><soap:Body><stopTransactionResponse xmlns="urn://Ocpp/Cs/2012/06/"/></soap:Body></soap:Envelope>'
        control = {
            'Action': 'StopTransaction',
            'MessageID': '6c9ec1cd-74d1-49a9-82d2-10dc46a29642',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': '509c8ce0-7e45-4c2d-920e-1ddcb7d39f21',
            'Type': message.RESULT,
            'Payload': {
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_heartbeat_req(self):
        """ Test HeartbeatRequest """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cs:chargeBoxIdentity>ABC</cs:chargeBoxIdentity><wsa5:MessageID>urn:uuid:f3795fcc-4dfd-4894-948e-ac8e7e9e1394</wsa5:MessageID><wsa5:From><wsa5:Address>http://192.168.0.102:8080/</wsa5:Address></wsa5:From><wsa5:ReplyTo><wsa5:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa5:Address></wsa5:ReplyTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://192.168.0.100:8080/steve/services/CentralSystemService</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/Heartbeat</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cs:heartbeatRequest></cs:heartbeatRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': 'f3795fcc-4dfd-4894-948e-ac8e7e9e1394',
            'From': 'http://192.168.0.102:8080/',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.100:8080/steve/services/CentralSystemService',
            'Type': message.CALL,
            'Action': 'Heartbeat',
            'Payload': {
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_heartbeat_res(self):
        """ Test HeartbeatResponse """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/HeartbeatResponse</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:6cdfd48f-d8fe-48a0-bd3f-16f5714b7c02</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://www.w3.org/2005/08/addressing/anonymous</To><RelatesTo xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:f3795fcc-4dfd-4894-948e-ac8e7e9e1394</RelatesTo></soap:Header><soap:Body><heartbeatResponse xmlns="urn://Ocpp/Cs/2012/06/"><currentTime>2018-09-14T07:19:58.894Z</currentTime></heartbeatResponse></soap:Body></soap:Envelope>'
        control = {
            'Action': 'Heartbeat',
            'MessageID': '6cdfd48f-d8fe-48a0-bd3f-16f5714b7c02',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': 'f3795fcc-4dfd-4894-948e-ac8e7e9e1394',
            'Type': message.RESULT,
            'Payload': {
                'currentTime': '2018-09-14T07:19:58.894Z'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_update_firmware_req(self):
        """ Test UpdateFirmwareRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/UpdateFirmware</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:b559f372-f34a-4986-ab9a-64056d956d68</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><updateFirmwareRequest xmlns="urn://Ocpp/Cp/2012/06/"><retrieveDate>2018-09-14T14:45:00.000Z</retrieveDate><location>http://192.168.0.100:8888</location><retries>1</retries><retryInterval>10</retryInterval></updateFirmwareRequest></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': 'b559f372-f34a-4986-ab9a-64056d956d68',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'UpdateFirmware',
            'Payload': {
                'retrieveDate': '2018-09-14T14:45:00.000Z',
                'location': 'http://192.168.0.100:8888',
                'retries': 1,
                'retryInterval': 10,
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_update_firmware_res(self):
        """ Test UpdateFirmwareResponse """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:b559f372-f34a-4986-ab9a-64056d956d68</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/UpdateFirmwareResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:updateFirmwareResponse></cp:updateFirmwareResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'UpdateFirmware',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': 'b559f372-f34a-4986-ab9a-64056d956d68',
            'Type': message.RESULT,
            'Payload': {
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_datatransfer_req(self):
        """ Test DataTransferRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/DataTransfer</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:44ee8dc0-ecd9-4beb-9aae-2d9514b5e2cf</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><dataTransferRequest xmlns="urn://Ocpp/Cp/2012/06/"><vendorId>stringid</vendorId><messageId>messageid</messageId><data>data-data-data</data></dataTransferRequest></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': '44ee8dc0-ecd9-4beb-9aae-2d9514b5e2cf',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'DataTransfer',
            'Payload': {
                'vendorId': 'stringid',
                'messageId': 'messageid',
                'data': 'data-data-data',
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_datatransfer_res(self):
        """ Test DataTransferResponse """
        " No testing data yet"
        self.assertEqual(True, True)

    def test_get_diagnostics_req(self):
        """ Test GetDiagnosticsRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/GetDiagnostics</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:aa91a2b7-bbfe-47d8-8c75-8d49c9ff7628</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><getDiagnosticsRequest xmlns="urn://Ocpp/Cp/2012/06/"><location>http://192.168.0.100:8888</location><startTime>2018-09-14T00:00:00.000Z</startTime><stopTime>2018-09-14T00:10:00.000Z</stopTime><retries>1</retries><retryInterval>10</retryInterval></getDiagnosticsRequest></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': 'aa91a2b7-bbfe-47d8-8c75-8d49c9ff7628',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'GetDiagnostics',
            'Payload': {
                'location': 'http://192.168.0.100:8888',
                'startTime': '2018-09-14T00:00:00.000Z',
                'stopTime': '2018-09-14T00:10:00.000Z',
                'retries': 1,
                'retryInterval': 10
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_get_diagnostics_res(self):
        """ Test GetDiagnosticsResponse """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:aa91a2b7-bbfe-47d8-8c75-8d49c9ff7628</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/GetDiagnosticsResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:getDiagnosticsResponse><cp:fileName>MaintenanceReport_2018_09_14_09_27_56.html.gz</cp:fileName></cp:getDiagnosticsResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'GetDiagnostics',
            'chargeBoxIdentity': 'ABC',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': 'aa91a2b7-bbfe-47d8-8c75-8d49c9ff7628',
            'Type': message.RESULT,
            'Payload': {
                'fileName': 'MaintenanceReport_2018_09_14_09_27_56.html.gz'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_unlock_connector_req(self):
        """ Test UnlockconnectorRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/UnlockConnector</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:59be0e44-40e0-4736-b73f-a40e5377bd30</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><unlockConnectorRequest xmlns="urn://Ocpp/Cp/2012/06/"><connectorId>1</connectorId></unlockConnectorRequest></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': '59be0e44-40e0-4736-b73f-a40e5377bd30',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'UnlockConnector',
            'Payload': {
                'connectorId': 1
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_unlock_connector_res(self):
        """ Test UnlockConnectorResponse """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:59be0e44-40e0-4736-b73f-a40e5377bd30</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/UnlockConnectorResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:unlockConnectorResponse><cp:status>Accepted</cp:status></cp:unlockConnectorResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'UnlockConnector',
            'chargeBoxIdentity': 'ABC',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': '59be0e44-40e0-4736-b73f-a40e5377bd30',
            'Type': message.RESULT,
            'Payload': {
                'status': 'Accepted'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_reset_req(self):
        """ Test ResetRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/Reset</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:d4b2442b-843a-46fa-80fb-e18ccc92a208</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><resetRequest xmlns="urn://Ocpp/Cp/2012/06/"><type>Hard</type></resetRequest></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': 'd4b2442b-843a-46fa-80fb-e18ccc92a208',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'Reset',
            'Payload': {
                'type': 'Hard'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_reset_res(self):
        """ Test ResetResponse """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:d4b2442b-843a-46fa-80fb-e18ccc92a208</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/ResetResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:resetResponse><cp:status>Accepted</cp:status></cp:resetResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'Reset',
            'chargeBoxIdentity': 'ABC',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': 'd4b2442b-843a-46fa-80fb-e18ccc92a208',
            'Type': message.RESULT,
            'Payload': {
                'status': 'Accepted'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_reset_res1(self):
        """ Test ResetRequest """
        data = b'<?xml version="1.0" encoding="UTF-8"?>\n<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>Magic</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:76398949-ca58-4518-bcc7-14d1d5193c04</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/ResetResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:resetResponse><cp:status>Accepted</cp:status></cp:resetResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>\r\n'
        control = {
            'chargeBoxIdentity': 'Magic',
            'RelatesTo': '76398949-ca58-4518-bcc7-14d1d5193c04',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'Type': message.RESULT,
            'Action': 'Reset',
            'Payload': {
                'status': 'Accepted'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_change_avail_req(self):
        """ Test ChangeAvailabilityRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/ChangeAvailability</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:e77b01bd-1e9f-4ecb-be94-277ab7022c94</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><changeAvailabilityRequest xmlns="urn://Ocpp/Cp/2012/06/"><connectorId>0</connectorId><type>Inoperative</type></changeAvailabilityRequest></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': 'e77b01bd-1e9f-4ecb-be94-277ab7022c94',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'ChangeAvailability',
            'Payload': {
                'connectorId': 0,
                'type': 'Inoperative'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_change_avail_res(self):
        """ Test ChangeAvailabilityResponse """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:e77b01bd-1e9f-4ecb-be94-277ab7022c94</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/ChangeAvailabilityResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:changeAvailabilityResponse><cp:status>Accepted</cp:status></cp:changeAvailabilityResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'ChangeAvailability',
            'chargeBoxIdentity': 'ABC',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': 'e77b01bd-1e9f-4ecb-be94-277ab7022c94',
            'Type': message.RESULT,
            'Payload': {
                'status': 'Accepted'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_clear_cache_req(self):
        """ Test ClearCacheRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/ClearCache</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:8f07707a-b370-44b7-9d5b-ba3facaad2f3</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><clearCacheRequest xmlns="urn://Ocpp/Cp/2012/06/"/></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': '8f07707a-b370-44b7-9d5b-ba3facaad2f3',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'ClearCache',
            'Payload': {
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_clear_cache_res(self):
        """ Test ChangeAvailabilityResponse """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:8f07707a-b370-44b7-9d5b-ba3facaad2f3</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/ClearCacheResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:clearCacheResponse><cp:status>Accepted</cp:status></cp:clearCacheResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'ClearCache',
            'chargeBoxIdentity': 'ABC',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': '8f07707a-b370-44b7-9d5b-ba3facaad2f3',
            'Type': message.RESULT,
            'Payload': {
                'status': 'Accepted'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_change_configuration_req(self):
        """ Test ChangeConfiguratioinRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/ChangeConfiguration</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:1a43a2cc-a4d0-41be-809e-d4c77b4f18dd</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><changeConfigurationRequest xmlns="urn://Ocpp/Cp/2012/06/"><key>HeartBeatInterval</key><value>10</value></changeConfigurationRequest></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': '1a43a2cc-a4d0-41be-809e-d4c77b4f18dd',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'ChangeConfiguration',
            'Payload': {
                'key': 'HeartBeatInterval',
                'value': '10'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_change_configuration_res(self):
        """ Test ChangeConfiguratioinResponse """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:1a43a2cc-a4d0-41be-809e-d4c77b4f18dd</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/ChangeConfigurationResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:changeConfigurationResponse><cp:status>Accepted</cp:status></cp:changeConfigurationResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'ChangeConfiguration',
            'chargeBoxIdentity': 'ABC',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': '1a43a2cc-a4d0-41be-809e-d4c77b4f18dd',
            'Type': message.RESULT,
            'Payload': {
                'status': 'Accepted'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_remote_start_req(self):
        """ Test RemoteStartTransactionRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/RemoteStartTransaction</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:34c39787-9605-47d3-8fc7-568e48e7dccf</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><remoteStartTransactionRequest xmlns="urn://Ocpp/Cp/2012/06/"><idTag>0700001B0BFA68</idTag><connectorId>1</connectorId></remoteStartTransactionRequest></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': '34c39787-9605-47d3-8fc7-568e48e7dccf',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'RemoteStartTransaction',
            'Payload': {
                'idTag': '0700001B0BFA68',
                'connectorId': 1
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_remote_start_res(self):
        """ Test RemoteStartTransactionResponse """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:34c39787-9605-47d3-8fc7-568e48e7dccf</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/RemoteStartTransactionResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:remoteStartTransactionResponse><cp:status>Accepted</cp:status></cp:remoteStartTransactionResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'RemoteStartTransaction',
            'chargeBoxIdentity': 'ABC',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': '34c39787-9605-47d3-8fc7-568e48e7dccf',
            'Type': message.RESULT,
            'Payload': {
                'status': 'Accepted'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_remote_stop_req(self):
        """ Test RemoteStopTransactionRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/RemoteStopTransaction</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:07766095-9622-47e4-8331-daf5a54418e0</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><remoteStopTransactionRequest xmlns="urn://Ocpp/Cp/2012/06/"><transactionId>27</transactionId></remoteStopTransactionRequest></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': '07766095-9622-47e4-8331-daf5a54418e0',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'RemoteStopTransaction',
            'Payload': {
                'transactionId': 27,
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_remote_stop_res(self):
        """ Test RemoteStopTransactionResponse """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:07766095-9622-47e4-8331-daf5a54418e0</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/RemoteStopTransactionResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:remoteStopTransactionResponse><cp:status>Accepted</cp:status></cp:remoteStopTransactionResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'RemoteStopTransaction',
            'chargeBoxIdentity': 'ABC',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': '07766095-9622-47e4-8331-daf5a54418e0',
            'Type': message.RESULT,
            'Payload': {
                'status': 'Accepted'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_cancel_reservation_req(self):
        """ Test CancelReservationRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/CancelReservation</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:28e0536e-67e5-4ed4-b94d-f62e2c2876d4</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><cancelReservationRequest xmlns="urn://Ocpp/Cp/2012/06/"><reservationId>7</reservationId></cancelReservationRequest></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': '28e0536e-67e5-4ed4-b94d-f62e2c2876d4',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'CancelReservation',
            'Payload': {
                'reservationId': 7

            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_cancel_reservation_res(self):
        """ Test CancelReservationResponse """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:28e0536e-67e5-4ed4-b94d-f62e2c2876d4</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/CancelReservationResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:cancelReservationResponse><cp:status>Accepted</cp:status></cp:cancelReservationResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'CancelReservation',
            'chargeBoxIdentity': 'ABC',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': '28e0536e-67e5-4ed4-b94d-f62e2c2876d4',
            'Type': message.RESULT,
            'Payload': {
                'status': 'Accepted'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_get_local_list_version_req(self):
        """ Test GetLocalListVersionRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/GetLocalListVersion</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:dcad6f9f-d6a4-431a-8f33-aad80b44a498</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><getLocalListVersionRequest xmlns="urn://Ocpp/Cp/2012/06/"/></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': 'dcad6f9f-d6a4-431a-8f33-aad80b44a498',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'GetLocalListVersion',
            'Payload': {
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_get_local_list_version_res(self):
        """ Test GetLocalListVersionResponse """
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:dcad6f9f-d6a4-431a-8f33-aad80b44a498</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/GetLocalListVersionResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:getLocalListVersionResponse><cp:listVersion>0</cp:listVersion></cp:getLocalListVersionResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'GetLocalListVersion',
            'chargeBoxIdentity': 'ABC',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': 'dcad6f9f-d6a4-431a-8f33-aad80b44a498',
            'Type': message.RESULT,
            'Payload': {
                'listVersion': 0
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_reserve_now_req(self):
        """ Test ReserveNowRequest """
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/ReserveNow</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:58d824ad-68bc-4035-8f9d-2da2522bcc36</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://192.168.0.102:8080/</To><ReplyTo xmlns="http://www.w3.org/2005/08/addressing"><Address>http://www.w3.org/2005/08/addressing/anonymous</Address></ReplyTo><chargeBoxIdentity xmlns="urn://Ocpp/Cp/2012/06/">ABC</chargeBoxIdentity></soap:Header><soap:Body><reserveNowRequest xmlns="urn://Ocpp/Cp/2012/06/"><connectorId>1</connectorId><expiryDate>2018-09-14T14:50:00.000Z</expiryDate><idTag>0700001B0BFA68</idTag><reservationId>7</reservationId></reserveNowRequest></soap:Body></soap:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': '58d824ad-68bc-4035-8f9d-2da2522bcc36',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.102:8080/',
            'Type': message.CALL,
            'Action': 'ReserveNow',
            'Payload': {
                'connectorId': 1,
                'expiryDate': '2018-09-14T14:50:00.000Z',
                'idTag': '0700001B0BFA68',
                'reservationId': 7
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_reserve_now_res(self):
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:58d824ad-68bc-4035-8f9d-2da2522bcc36</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/ReserveNowResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:reserveNowResponse><cp:status>Accepted</cp:status></cp:reserveNowResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'Action': 'ReserveNow',
            'chargeBoxIdentity': 'ABC',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': '58d824ad-68bc-4035-8f9d-2da2522bcc36',
            'Type': message.RESULT,
            'Payload': {
                'status': 'Accepted'
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_meters1_req(self):
        """ Test MeterValues [Single]"""
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cs:chargeBoxIdentity>ABC</cs:chargeBoxIdentity><wsa5:MessageID>urn:uuid:d0231b25-f293-4d7d-aff7-82f5a7c7b21c</wsa5:MessageID><wsa5:From><wsa5:Address>http://192.168.0.102:8080/</wsa5:Address></wsa5:From><wsa5:ReplyTo><wsa5:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa5:Address></wsa5:ReplyTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://192.168.0.100:8080/steve/services/CentralSystemService</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/MeterValues</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cs:meterValuesRequest><cs:connectorId>1</cs:connectorId><cs:transactionId>29</cs:transactionId><cs:values><cs:timestamp>2018-09-14T10:04:05Z</cs:timestamp><cs:value unit="Wh" location="Outlet" measurand="Energy.Active.Import.Register" format="Raw" context="Sample.Periodic">0</cs:value></cs:values></cs:meterValuesRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'chargeBoxIdentity': 'ABC',
            'MessageID': 'd0231b25-f293-4d7d-aff7-82f5a7c7b21c',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://192.168.0.100:8080/steve/services/CentralSystemService',
            'Type': message.CALL,
            'Action': 'MeterValues',
            'Payload': {
                'values': [{
                    'timestamp': '2018-09-14T10:04:05Z',
                    'values': [{'value': '0',
                                'unit': 'Wh',
                                'location': 'Outlet',
                                'measurand': 'Energy.Active.Import.Register',
                                'format': 'Raw',
                                'context': 'Sample.Periodic',
                                }]
                }],

                'connectorId': 1,
                'transactionId': 29,
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_meters2_req(self):
        """ Test MeterValues [Multi]"""
        data = b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:ocppCp15="urn://Ocpp/Cp/2012/06/" xmlns:ocppCs15="urn://Ocpp/Cs/2012/06/" xmlns:wsa5="http://www.w3.org/2005/08/addressing"><SOAP-ENV:Header><ocppCs15:chargeBoxIdentity>TEST1</ocppCs15:chargeBoxIdentity><wsa5:MessageID>urn:uuid:1537863095789</wsa5:MessageID><wsa5:From><wsa5:Address>http://localhost:6161</wsa5:Address></wsa5:From><wsa5:ReplyTo><wsa5:Address>http://www.w3.org/2005/08/addressing/anonymous</wsa5:Address></wsa5:ReplyTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://127.0.0.1:8080/ocpp</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/MeterValues</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><ocppCs15:meterValuesRequest><ocppCs15:connectorId>1</ocppCs15:connectorId><ocppCs15:transactionId></ocppCs15:transactionId><ocppCs15:values><ocppCs15:timestamp>2018-09-25T08:11:36.000Z</ocppCs15:timestamp><ocppCs15:value>95</ocppCs15:value><ocppCs15:value>95</ocppCs15:value><ocppCs15:value>95</ocppCs15:value><ocppCs15:value>95</ocppCs15:value></ocppCs15:values><ocppCs15:values><ocppCs15:timestamp>2018-09-25T08:11:36.000Z</ocppCs15:timestamp><ocppCs15:value unit="Wh" location="Outlet" measurand="Energy.Active.Import.Register" format="Raw" context="Sample.Periodic">95</ocppCs15:value></ocppCs15:values><ocppCs15:values><ocppCs15:timestamp>2018-09-25T08:11:36.000Z</ocppCs15:timestamp><ocppCs15:value unit="Wh" location="Outlet" measurand="Energy.Active.Import.Register" format="Raw" context="Sample.Periodic">95</ocppCs15:value></ocppCs15:values><ocppCs15:values><ocppCs15:timestamp>2018-09-25T08:11:36.000Z</ocppCs15:timestamp><ocppCs15:value unit="Wh" location="Outlet"  format="Raw" >95</ocppCs15:value></ocppCs15:values><ocppCs15:values><ocppCs15:timestamp>2018-09-25T08:11:36.000Z</ocppCs15:timestamp><ocppCs15:value unit="Wh" location="Outlet" measurand="Energy.Active.Import.Register" format="Raw" context="Sample.Periodic">95</ocppCs15:value></ocppCs15:values><ocppCs15:values><ocppCs15:timestamp>2018-09-25T08:11:36.000Z</ocppCs15:timestamp><ocppCs15:value unit="Wh" location="Outlet" measurand="Energy.Active.Import.Register" format="Raw" context="Sample.Periodic">95</ocppCs15:value></ocppCs15:values><ocppCs15:values><ocppCs15:timestamp>2018-09-25T08:11:36.000Z</ocppCs15:timestamp><ocppCs15:value unit="Wh" location="Outlet" measurand="Energy.Active.Import.Register"  context="Sample.Periodic">95</ocppCs15:value></ocppCs15:values><ocppCs15:values><ocppCs15:timestamp>2018-09-25T08:11:36.000Z</ocppCs15:timestamp><ocppCs15:value unit="Wh" location="Outlet" measurand="Energy.Active.Import.Register" format="Raw" context="Sample.Periodic">95</ocppCs15:value></ocppCs15:values><ocppCs15:values><ocppCs15:timestamp>2018-09-25T08:11:36.000Z</ocppCs15:timestamp><ocppCs15:value unit="Wh" location="Outlet" measurand="Energy.Active.Import.Register"  context="Sample.Periodic">95</ocppCs15:value></ocppCs15:values><ocppCs15:values><ocppCs15:timestamp>2018-09-25T08:11:36.000Z</ocppCs15:timestamp><ocppCs15:value unit="Wh" location="Outlet" measurand="Energy.Active.Import.Register" format="Raw" context="Sample.Periodic">95</ocppCs15:value></ocppCs15:values></ocppCs15:meterValuesRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        control = {
            'chargeBoxIdentity': 'TEST1',
            'MessageID': '1537863095789',
            'ReplyTo': 'http://www.w3.org/2005/08/addressing/anonymous',
            'To': 'http://127.0.0.1:8080/ocpp',
            'Type': message.CALL,
            'Action': 'MeterValues',
            'Payload': {
                'values': [{'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95'}, {'value': '95'}, {'value': '95'}, {'value': '95'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'format': 'Raw'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}],
                'connectorId': 1,
                'transactionId': 0,
            }
        }
#
#        #{'meterValuesRequest': {'connectorId': 1, 'values': [{'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95'}, {'value': '95'}, {'value': '95'}, {'value': '95'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'format': 'Raw'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'context': 'Sample.Periodic'}]}, {'timestamp': '2018-09-25T08:11:36.000Z', 'values': [{'value': '95', 'unit': 'Wh', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'format': 'Raw', 'context': 'Sample.Periodic'}]}]}}
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)

    def test_meters_res(self):
        data = b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header><Action xmlns="http://www.w3.org/2005/08/addressing">/MeterValuesResponse</Action><MessageID xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:49bebcee-9e44-42d7-9e43-83b0acba5137</MessageID><To xmlns="http://www.w3.org/2005/08/addressing">http://www.w3.org/2005/08/addressing/anonymous</To><RelatesTo xmlns="http://www.w3.org/2005/08/addressing">urn:uuid:d0231b25-f293-4d7d-aff7-82f5a7c7b21c</RelatesTo></soap:Header><soap:Body><meterValuesResponse xmlns="urn://Ocpp/Cs/2012/06/"/></soap:Body></soap:Envelope>'
        control = {
            'Action': 'MeterValues',
            'MessageID': '49bebcee-9e44-42d7-9e43-83b0acba5137',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': 'd0231b25-f293-4d7d-aff7-82f5a7c7b21c',
            'Type': message.RESULT,
            'Payload': {
            }
        }
        msg = parser.parse(data)
        self.assertTrue(message.validate(msg))
        for (key, value) in control.items():
            self.assertEqual(msg[key], value)
