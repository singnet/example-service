FROM ubuntu:18.04

ENV SINGNET_REPOS=/opt/singnet

RUN mkdir -p ${SINGNET_REPOS}

RUN apt-get update && \
    apt-get install -y \
    nano \
    git \
    wget

RUN apt-get install -y python3 python3-pip

RUN cd ${SINGNET_REPOS} && \
    mkdir snet-daemon && \
    cd snet-daemon && \
    wget https://github.com/singnet/snet-daemon/releases/download/v0.1.4/snetd-0.1.4.tar.gz && \
    tar -xvf snetd-0.1.4.tar.gz && \
    mv snetd-0.1.4/snetd-linux-amd64 /usr/bin/snetd

RUN cd ${SINGNET_REPOS} && \
    git clone https://github.com/singnet/example-service.git && \
    cd example-service && \
    pip3 install -r requirements.txt && \
    sh buildproto.sh

WORKDIR ${SINGNET_REPOS}/example-service
