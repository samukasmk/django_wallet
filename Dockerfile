FROM python:3.11.3-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y make gcc python-dev libpq-dev && \
    apt clean && \
    apt autoclean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/belvo_wallet

COPY . /opt/belvo_wallet

RUN make install
RUN make collectstatic
