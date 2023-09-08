FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get -q update \
    && apt-get -q -y --no-install-recommends install libev4 libev-dev gcc libc6-dev

WORKDIR /opt/test

COPY ./src/requirements.txt ./requirements.txt

RUN --mount=type=cache,target=~/.cache/pip \
    pip install --upgrade pip wheel \
    && pip install -r requirements.txt
#
RUN apt-get -q -y purge libev-dev gcc libc6-dev \
    && apt-get -q -y autoremove \
    && apt-get -q -y clean \
    && apt-get -q -y autoclean\
    && apt-get -q -y  install wget
#
COPY ./src/. ./

ENTRYPOINT ["python", "main.py"]
