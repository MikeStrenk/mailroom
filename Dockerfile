FROM python:3.7

COPY requirements.txt ./

RUN pip install -r requirements.txt

WORKDIR /usr/src/mailroom

COPY . /usr/src/mailroom

RUN /bin/bash