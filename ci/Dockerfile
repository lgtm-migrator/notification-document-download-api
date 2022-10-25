FROM python:3.9-alpine@sha256:7311322d0f836872da01e8affcd58cadc6e0d94f5777e76579fdbf14cd38d5ab

ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --no-cache build-base git gcc make libffi-dev openssl-dev libmagic && rm -rf /var/cache/apk/*

# update pip
RUN python -m pip install wheel

RUN set -ex && mkdir /app

WORKDIR /app

COPY . /app

RUN set -ex && pip3 install -r requirements.txt

ENV PORT=7000

CMD ["sh", "-c", "gunicorn -c gunicorn_config.py application"]
