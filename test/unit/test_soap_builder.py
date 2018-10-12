""" Tests for SOAP parser"""
import unittest
import tom.soap.parser.base as parser
import tom.soap.builder.base as builder
from tom.ocpp import message


class SOAPBuilderTest(unittest.TestCase):
    """ Base builder's tests
    Не совсем чистые тесты, т.к. для проверки билдера используется парсер. Но в данном
    случае это наименьшее зло и это точно лучше чем отсутсвие тестов. Так что следует помнить
    об этой зависимости (если парсер косой, то тесты билдера будут автоматом некорректны)
    """

    def test_boot_notification_req(self):
        """ Test BootNotificationRequest """
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
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_boot_notification_res(self):
        """ Test BootNotificationResponse """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_authorize_req(self):
        """ Test AuthorizeRequest """
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
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_authorize_res(self):
        """ Test AuthorizeResponse """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_status_notification_req(self):
        """ Test StatusNotificationRequest """
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
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_status_notification_res(self):
        """ Test StatusNotificationResponse """
        control = {
            'Action': 'StatusNotification',
            'MessageID': '39736d2b-551e-486e-a820-bed4c702bf9d',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': 'a6fe232d-b29f-4b1c-b127-09752124d2b7',
            'Type': message.RESULT,
            'Payload': {
            }
        }
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_start_transaction_req(self):
        """ Test StartTransactionRequest """
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
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_start_transaction_res(self):
        """ Test StatusNotificationRequest """
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
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_stop_transaction_req(self):
        """ Test StopTransactionRequest """
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
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_stop_transaction_res(self):
        """ Test StopNotificationRequest """
        control = {
            'Action': 'StopTransaction',
            'MessageID': '6c9ec1cd-74d1-49a9-82d2-10dc46a29642',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': '509c8ce0-7e45-4c2d-920e-1ddcb7d39f21',
            'Type': message.RESULT,
            'Payload': {
            }
        }
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_heartbeat_req(self):
        """ Test HeartbeatRequest """
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
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_heartbeat_res(self):
        """ Test HeartbeatResponse """
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
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_update_firmware_req(self):
        """ Test UpdateFirmwareRequest """
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
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_update_firmware_res(self):
        """ Test UpdateFirmwareResponse """
        control = {
            'Action': 'UpdateFirmware',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': 'b559f372-f34a-4986-ab9a-64056d956d68',
            'Type': message.RESULT,
            'Payload': {
            }
        }
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_datatransfer_req(self):
        """ Test DataTransferRequest """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_datatransfer_res(self):
        """ Test DataTransferResponse """
        " No testing data yet"
        self.assertEqual(True, True)

    def test_get_diagnostics_req(self):
        """ Test GetDiagnosticsRequest """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_get_diagnostics_res(self):
        """ Test GetDiagnosticsResponse """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_meters_res(self):
        control = {
            'Action': 'MeterValues',
            'MessageID': '49bebcee-9e44-42d7-9e43-83b0acba5137',
            'To': 'http://www.w3.org/2005/08/addressing/anonymous',
            'RelatesTo': 'd0231b25-f293-4d7d-aff7-82f5a7c7b21c',
            'Type': message.RESULT,
            'Payload': {
            }
        }

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_unlock_connector_req(self):
        """ Test UnlockconnectorRequest """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_unlock_connector_res(self):
        """ Test UnlockConnectorResponse """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_reset_req(self):
        """ Test ResetRequest """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_reset_res(self):
        """ Test ResetResponse """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_change_avail_req(self):
        """ Test ChangeAvailabilityRequest """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_change_avail_res(self):
        """ Test ChangeAvailabilityResponse """
        data = '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:e77b01bd-1e9f-4ecb-be94-277ab7022c94</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/ChangeAvailabilityResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:changeAvailabilityResponse><cp:status>Accepted</cp:status></cp:changeAvailabilityResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_clear_cache_req(self):
        """ Test ClearCacheRequest """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_clear_cache_res(self):
        """ Test ChangeAvailabilityResponse """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_change_configuration_req(self):
        """ Test ChangeConfiguratioinRequest """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_change_configuration_res(self):
        """ Test ChangeConfiguratioinResponse """
        data = '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cp="urn://Ocpp/Cp/2012/06/" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:cs="urn://Ocpp/Cs/2012/06/"><SOAP-ENV:Header><cp:chargeBoxIdentity>ABC</cp:chargeBoxIdentity><wsa5:RelatesTo>urn:uuid:1a43a2cc-a4d0-41be-809e-d4c77b4f18dd</wsa5:RelatesTo><wsa5:To SOAP-ENV:mustUnderstand="true">http://www.w3.org/2005/08/addressing/anonymous</wsa5:To><wsa5:Action SOAP-ENV:mustUnderstand="true">/ChangeConfigurationResponse</wsa5:Action></SOAP-ENV:Header><SOAP-ENV:Body><cp:changeConfigurationResponse><cp:status>Accepted</cp:status></cp:changeConfigurationResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>'
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_remote_start_req(self):
        """ Test RemoteStartTransactionRequest """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_remote_start_res(self):
        """ Test RemoteStartTransactionResponse """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_remote_stop_req(self):
        """ Test RemoteStopTransactionRequest """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_remote_stop_res(self):
        """ Test RemoteStopTransactionResponse """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_cancel_reservation_req(self):
        """ Test CancelReservationRequest """
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
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_cancel_reservation_res(self):
        """ Test CancelReservationResponse """
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
        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_get_local_list_version_req(self):
        """ Test GetLocalListVersionRequest """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_get_local_list_version_res(self):
        """ Test GetLocalListVersionResponse """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_reserve_now_req(self):
        """ Test ReserveNowRequest """
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)

    def test_reserve_now_res(self):
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

        soap = builder.build(control)
        ocpp = parser.parse(soap)
        for (key, value) in control.items():
            self.assertEqual(ocpp[key], value)
