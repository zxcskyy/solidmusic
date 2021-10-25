FROM python:3.9.7-slim-buster
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install git curl python3-pip ffmpeg -y \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install nodejs -y \
    && npm i -g npm \
    && pip3 install --no-cache-dir -U pip \
COPY . /app
WORKDIR /app
RUN pip3 install --no-cache-dir -U -r requirements.txt
CMD python3 main.py
