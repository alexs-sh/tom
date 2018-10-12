## Конвертер OCPP (SOAP) <-> OCPP (JSON)

### Описание
Конвертер позволяет подключать зарядные станции с OCPP (SOAP) к центральным системам с поддержкой OCPP (JSON)

### Зависимости
- python3
- lxml
- twisted
- autobahn

### Быстрый старт

    	python main.py --port=8888 --url=ws://192.168.56.101:8080/steve/websocket/CentralSystemService

- port - номер порта для подключений от ЗС
- url - адрес ЦС

Доп. параметры запуска можно вывести при помощи команды:

    	python main.py --help
 
	
### Запуск в virtualenv в Debain 9
    	# apt update
		# apt install git python3 python3-pip python3-virtualenv
		$ git clone <project repo>
		$ cd tom
		$ python3 -m virtualenv --python=python3 .
		$ source bin/activate
		$ pip3 install lxml twisted autobahn
		$ python main.py --port=8888 --url=ws://192.168.56.101:8080/steve/websocket/CentralSystemService

		
### Перечень поддерживаемых сообщений OCPP 1.5

    CentralSystem
    | Message                                                           | SOAP Parser  | SOAP Builder |
    | ---                                                               | ---          | ---          |
    | AuthorizeReq                                                      | OK           | OK           |
    | AuthorizeRes                                                      | OK           | OK           |
    | StartTransactionReq                                               | OK           | OK           |
    | StartTransactionRes                                               | OK           | OK           |
    | StopTransactionReq                                                | OK           | OK           |
    | StopTransactionRes                                                | OK           | OK           |
    | HeartbeatReq                                                      | OK           | OK           |
    | HeartbeatRes                                                      | OK           | OK           |
    | MeterValuesReq                                                    | OK           |           NO |
    | MeterValuesRes                                                    | OK           | OK           |
    | BootNotificationReq                                               | OK           | OK           |
    | BootNotificationRes                                               | OK           | OK           |
    | StatusNotificationReq                                             | OK           | OK           |
    | StatusNotificationRes                                             | OK           | OK           |
    | FirmwareStatusNotificationReq                                     | ?            | ?            |
    | FirmwareStatusNotificationRes                                     | ?            | ?            |
    | DiagnosticsStatusNotificationReq                                  | ?            | ?            |
    | DiagnosticsStatusNotificationRes                                  | ?            | ?            |
    | DataTransferReq                                                   | OK           | OK           |
    | DataTransferRes                                                   | ?            | ?            |

    ChargePoint
    | UnlockConnectorReq                                                | OK           | OK           |
    | UnlockConnectorRes                                                | OK           | OK           |
    | ResetReq                                                          | OK           | OK           |
    | ResetRes                                                          | OK           | OK           |
    | ChangeAvailabilityReq                                             | OK           | OK           |
    | ChangeAvailabilityRes                                             | OK           | OK           |
    | GetDiagnosticsReq                                                 | OK           | OK           |
    | GetDiagnosticsRes                                                 | OK           | OK           |
    | ClearCacheReq                                                     | OK           | OK           |
    | ClearCacheRes                                                     | OK           | OK           |
    | UpdateFirmwareReq                                                 | OK           | OK           |
    | UpdateFirmwareRes                                                 | OK           | OK           |
    | ChangeConfigurationReq                                            | OK           | OK           |
    | ChangeConfigurationRes                                            | OK           | OK           |
    | RemoteStartTransactionReq                                         | OK           | OK           |
    | RemoteStartTransactionRes                                         | OK           | OK           |
    | RemoteStopTransactionReq                                          | OK           | OK           |
    | RemoteStopTransactionRes                                          | OK           | OK           |
    | CancelReservationReq                                              | OK           | OK           |
    | CancelReservationRes                                              | OK           | OK           |
    | GetConfigurationReq                                               |           NO |           NO |
    | GetConfigurationRes                                               |           NO |           NO |
    | GetLocalListVersionReq                                            | OK           | OK           |
    | GetLocalListVersionRes                                            | OK           | OK           |
    | ReserveNowReq                                                     | OK           | OK           |
    | ReserveNowRes                                                     | OK           | OK           |
    | SendLocalListReq                                                  |           NO |           NO |          
    | SendLocalListRes                                                  |           NO |           NO |
