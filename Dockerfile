FROM ubuntu:18.04

ENV SINGNET_REPOS=/opt/singnet

RUN mkdir -p ${SINGNET_REPOS}

RUN apt-get update && \
    apt-get install -y \
    curl \
    nano \
    git \
    wget

RUN apt-get install -y python3 python3-pip

RUN SNETD_VERSION=`curl -s https://api.github.com/repos/singnet/snet-daemon/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")'` && \
    cd /tmp && \
    wget https://github.com/singnet/snet-daemon/releases/download/${SNETD_VERSION}/snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    tar -xvf snet-daemon-${SNETD_VERSION}-linux-amd64.tar.gz && \
    mv snet-daemon-${SNETD_VERSION}-linux-amd64/snetd /usr/bin/snetd

RUN cd ${SINGNET_REPOS} && \
    git clone https://github.com/singnet/example-service.git && \
    cd example-service && \
    pip3 install -r requirements.txt && \
    sh buildproto.sh

WORKDIR ${SINGNET_REPOS}/example-service
