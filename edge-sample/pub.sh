#! /bin/bash

for((i=1;i<=10;i++));
do
    temper=$(($RANDOM%100))
    mosquitto_pub -h 192.168.1.172 -m "{\"devid\": \"demo1\", \"temperature\": $temper}" -t devices/device_001/messages;
done