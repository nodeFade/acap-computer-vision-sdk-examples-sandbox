#!/bin/bash

# ok=$(curl -s --noproxy '*' --anyauth -u root:"pass" -k --header "Content-Type: application/json" --request POST --data '{"apiVersion":"1.0","method":"getProperties", "params": {"propertyList": ["Architecture"]}}' http://172.25.70.46/axis-cgi/basicdeviceinfo.cgi)
# echo  "response from curl= $ok" 
# ok=${ok#*Architecture}
# echo "test=$(echo $ok | cut -d '"' -f 3)" >> $GITHUB_ENV
# echo ok=$(echo $ok | cut -d '"' -f 3)

# ok=$(curl -s --noproxy '*' --anyauth -u root:"pass" -k --header "Content-Type: application/json" --request POST --data '{"apiVersion":"1.0","method":"getProperties", "params": {"propertyList": ["Architecture"]}}' http://172.25.65.98/axis-cgi/basicdeviceinfo.cgi)
# echo  "response from curl= $ok" 
# ok=${ok#*Architecture}
# echo "test=$(echo $ok | cut -d '"' -f 3)" >> $GITHUB_ENV
# echo ok=$(echo $ok | cut -d '"' -f 3)


for i in {1..5}; do
    sleep 1
    echo $i
done