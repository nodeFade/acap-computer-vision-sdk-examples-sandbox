#!/bin/bash


# for i in {1..5}; do
#     sleep 1
#     echo $i
# done


curl -v -s --anyauth -u root:"pass" "http://172.25.65.98/axis-cgi/param.cgi?action=update&root.Network.SSH.Enabled=yes"
ssh root@172.25.65.98 'command -v containerd >/dev/null 2>&1 && echo Compatible with Docker ACAP || echo Not compatible with Docker ACAP'
curl -v -s --anyauth -u root:"pass" -k --header "Content-Type:application/json" http://172.25.65.98/axis-cgi/admin/systemlog.cgi?