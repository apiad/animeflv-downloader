FROM ubuntu:20.04

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y gpac firefox python3-pip
COPY requirements.txt /src/requirements.txt
WORKDIR /src
RUN python3 -m pip install -r requirements.txt

COPY . /src
