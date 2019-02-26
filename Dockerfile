FROM ubuntu:18.04

ARG snetd_version="v0.1.7"

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
    wget https://github.com/singnet/snet-daemon/releases/download/${snetd_version}/snet-daemon-${snetd_version}-linux-amd64.tar.gz && \
    tar -xvf snet-daemon-${snetd_version}-linux-amd64.tar.gz && \
    mv snet-daemon-${snetd_version}-linux-amd64/snetd /usr/bin/snetd

RUN cd ${SINGNET_REPOS} && \
    git clone https://github.com/singnet/example-service.git && \
    cd example-service && \
    pip3 install -r requirements.txt && \
    sh buildproto.sh

WORKDIR ${SINGNET_REPOS}/example-service
