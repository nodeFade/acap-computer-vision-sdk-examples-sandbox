#!/bin/bash
HOST=$1
IP=$1
PASS='pass'
LOCATION=$2
##################### KEY AND CSR ########################
# Generate CA private and public keys:
echo "Step 1: Generate CA private keys"
openssl genrsa -passout pass:'pass' -aes256 -out ca-key.pem 4096
echo "Step 2: Generate CA public keys"
openssl req -new -passin pass:'pass' -x509 -days 365 -key ca-key.pem -sha256 << ANSWERS -out ca.pem
US
IL
Chicago
Myself
Me
*.dev
admin@localhost
ANSWERS

#################### SERVER ############################
# Create a server key and certificate signing request (CSR). Make sure that “Common Name” matches the hostname of the camera:
echo "Step 3: Generate Server keys"
openssl genrsa -out server-key.pem 4096
echo "Step 4: Generate Signing Request"
openssl req -subj "/CN=$HOST" -sha256 -new -key server-key.pem -out server.csr
# Sign the public key with our CA:
# TLS connections can be made through IP address as well as DNS name, the IP addresses need to be specified when creating the certificate.
echo subjectAltName = DNS:$HOST,IP:$IP,IP:127.0.0.1 >> extfile.cnf
# Set the Docker daemon key’s extended usage attributes to be used only for server authentication:
echo extendedKeyUsage = serverAuth >> extfile.cnf
#Generate the signed certificate:
echo "Step 5: Generate Server Signed Certificate"
openssl x509 -req -passin pass:'pass' -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
    -CAcreateserial -out server-cert.pem -extfile extfile.cnf

################ CLIENT ##############################
# For client authentication, create a client key and certificate signing request:
echo "Step 6: Generate Client key"
openssl genrsa -out key.pem 4096
echo "Step 7: Generate Client CSR"
openssl req -subj '/CN=client' -new -key key.pem -out client.csr
# To make the key suitable for client authentication, create a new extensions config file:
echo extendedKeyUsage = clientAuth > extfile-client.cnf
# Generate the signed certificate:
echo "Step 8: Generate Client Signed Certificate"
openssl x509 -req -passin pass:'pass' -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem \
    -CAcreateserial -out cert.pem -extfile extfile-client.cnf
################## MOVE AND CLEANUP FILES #######################
# The two certificate signing requests and extensions config files can now be removes:
rm -v client.csr server.csr extfile.cnf extfile-client.cnf

# Protect the keys from accidental damage, and or reading by anyone else:
chmod -v 0400 ca-key.pem server-key.pem
chmod -v 0444 ca.pem server-cert.pem cert.pem key.pem
# Verify ssh is enabled on host:
curl -s --noproxy "*" --anyauth -u root:$PASS "http://$HOST/axis-cgi/param.cgi?action=update&Network.SSH.Enabled=yes"
# Make the Docker daemon only accept connections from clients providing a certificate trusted by your CA:
echo "Step 9: Copy certificate to DUT"
# sshpass -v -p $PASS scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ca.pem server-cert.pem server-key.pem root@$HOST:/usr/local/packages/$LOCATION
# scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ca.pem server-cert.pem server-key.pem root@172.25.65.98:/usr/local/packages/dockerdwrapper/