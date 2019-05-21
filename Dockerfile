FROM ubuntu

MAINTAINER Ryota Sakamoto <saka_ro@yahoo.co.jp>


COPY . /usr/src/ogc-poc1-device
WORKDIR /usr/src/ogc-poc1-device

RUN mv /bin/sh /bin/sh_tmp && ln -s /bin/bash /bin/sh

RUN apt-get update && apt-get upgrade -y && \
    apt-get install python3-dev -y && \
    apt-get install python3-pip -y && \
    pip3 install --user -r requirements/common.txt
