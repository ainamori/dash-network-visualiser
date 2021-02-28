FROM python:3.9-buster

LABEL name="dash-network-visualiser"
LABEL version="1.0.0"
LABEL architecture="x86_64"

RUN apt-get update \
  && apt-get install -y tzdata vim curl net-tools procps libpq5 libxml2 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY ./app.py /opt/app.py
COPY ./modules /opt/modules
COPY ./style /opt/style
COPY ./requirements.txt /opt/requirements.txt
RUN pip3 install -r /opt/requirements.txt
