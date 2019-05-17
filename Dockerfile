FROM hypriot/rpi-node:latest

MAINTAINER Ryota Sakamoto <saka_ro@yahoo.co.jp>

COPY . /usr/src/ogc-poc1-device
WORKDIR /usr/src/ogc-poc1-device

RUN apt-get update && apt-get upgrade -y && \
    apt-get install python3-dev -y && \
    apt-get install python3-pip -y && \
    pip3 install --user -r requirements/common.txt
