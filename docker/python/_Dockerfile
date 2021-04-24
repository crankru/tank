FROM python:3.8.8-buster

ENV DOCKER=1 PYTHONUNBUFFERED=1 DEBIAN_FRONTEND=noninteractive 
# Picamera install
ENV READTHEDOCS=True

# VOLUME /tmp

RUN apt-get update && apt-get install -y i2c-tools build-essential cmake sudo gcc \
    && pip install pip-tools \
    # build userland
    && cd /tmp && git clone https://github.com/raspberrypi/userland.git \
    && cd userland/ && ./buildme \
    && ln -s /tmp/userland/build/bin/vcgencmd /usr/bin/vcgencmd \
    && echo '/opt/vc/lib' > /etc/ld.so.conf.d/vc.conf ; ldconfig \
    && apt-get clean

ADD requirements.txt /requirements.txt
ADD requirements.in /requirements.in

RUN pip-compile --generate-hashes --reuse-hashes --verbose /requirements.in
RUN pip install -r /requirements.txt

# RUN apt-get install -y python3-numpy python3-opencv libopencv-contrib-dev \
#     && apt-get clean

RUN pip3 install numpy
# RUN pip install numpy==1.20.1
RUN pip3 install opencv-python
# RUN pip install opencv-python==4.5.1.48
RUN pip3 install opencv-contrib-python

WORKDIR /code