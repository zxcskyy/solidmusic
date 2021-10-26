FROM python:3.9.7-slim-buster
RUN apt-get update \
    && apt-get install -y --no-install-recommends git=2.33.1 curl=7.79.1 python3-pip=21.3 ffmpeg=4.2.5 \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y --no-install-recommends nodejs=16.12.0 \
    && npm i -g npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . /app
WORKDIR /app
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt
CMD python3 main.py
