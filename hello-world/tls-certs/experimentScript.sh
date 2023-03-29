#!/bin/bash

# export APP_NAME=hello-world
# export ARCH=aarch64

# docker build --tag $APP_NAME --build-arg $ARCH .
# DEVICE_IP=172.25.65.98
# DEVICE_PASSWORD='pass'
# ARCH=aarch64

# curl -s --anyauth -u root:"pass" "http://172.25.65.98/axis-cgi/param.cgi?action=update&root.Network.SSH.Enabled=yes" 
# ssh root@172.25.65.98 'command -v containerd >/dev/null 2>&1 && echo Compatible with Docker ACAP || echo Not compatible with Docker ACAP' 

# docker run --rm axisecp/docker-acap:latest-$ARCH $DEVICE_IP $DEVICE_PASSWORD install
# curl -s --anyauth -u "root:$DEVICE_PASSWORD" "http://$DEVICE_IP/axis-cgi/param.cgi?action=update&root.dockerdwrapper.UseTLS=yes"


# cd hello-world/tls-certs
# scp ca.pem server-cert.pem server-key.pem root@$DEVICE_IP:/usr/local/packages/dockerdwrapper/

# sshpass -p 'pass' scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ca.pem server-cert.pem server-key.pem root@172.25.65.98:/usr/local/packages/dockerdwrapper/
ok=$(curl -v -s --noproxy '*' --anyauth -u root:"pass" -k --header "Content-Type: application/json" --request POST --data '{"apiVersion":"1.0", "method":"getProperties", "params": {"propertyList": ["Architecture"]}}' http://172.25.70.46//axis-cgi/basicdeviceinfo.cgi)
echo  "response from curl= $ok" 