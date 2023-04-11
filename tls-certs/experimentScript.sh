#!/bin/bash


# for i in {1..5}; do
#     sleep 1
#     echo $i
# done

# alias "images"="docker images -a"
# image: axisecp/acap-computer-vision-sdk:latest-aarch64-runtime

docker images -a
docker image inspect --format='{{.RepoDigests}}' axisecp/acap-computer-vision-sdk:latest-aarch64-runtime
docker save axisecp/acap-computer-vision-sdk:latest-aarch64-runtime -o  axisecp/acap-computer-vision-sdk:latest-aarch64-runtime.tar
sha256sum axisecp/acap-computer-vision-sdk:latest-aarch64-runtime.tar
docker rmi axisecp/acap-computer-vision-sdk:latest-aarch64-runtime.tar