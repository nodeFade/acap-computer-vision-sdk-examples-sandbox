export APP_NAME=hello-world
export ARCH=aarch64

docker build --tag $APP_NAME --build-arg $ARCH .