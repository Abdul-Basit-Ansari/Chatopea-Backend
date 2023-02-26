FROM ubuntu:20.04


WORKDIR /app
ADD ./requirements.txt /app/requirements.txt


RUN export DEBIAN_FRONTEND=noninteractive && \
apt-get update && \
apt-get upgrade -yq && \
apt-get -yq install \
python3 python3-pip default-libmysqlclient-dev zip git tzdata && \
pip3 install --no-cache-dir -r requirements.txt

RUN apt-get clean autoclean && \
apt-get autoremove -y && \
rm -rf /var/lib/{apt,dpkg,cache,log}/

