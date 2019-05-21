# OGC POC1 DEVICE

In this project, Raspbery pi LED and button communicate with fiware via MQTT.

## Getting Started

### Run dest_button

```
$ nohup  ./dest_button.py --host 'mqtt.host.jp' --port 8883 --ssl --key_file './ssl/DST_Root_CA_X3.pem' --device_type button --device_id button_01 --username xxxxxx --password xxxxx &
```


### Run dest_led

```
$ nohup  ./dest_led.py --host 'mqtt.host.jp' --port 8883 --ssl --key_file './ssl/DST_Root_CA_X4.pem' --device_type button --device_id button_01 --username xxxxxx --password xxxxx &
```

### Run entrance_button 

```
$ nohup  ./entrance_button.py --host 'mqtt.host.jp' --port 8883 --ssl --key_file './ssl/DST_Root_CA_X3.pem' --device_type button --device_id button_01 --username xxxxxx --password xxxxx &
```

## License

[Apache License 2.0](/LICENSE)

## Copyright
Copyright (c) 2018 TIS Inc.
