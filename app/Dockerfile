FROM rust:latest

WORKDIR /app

RUN apt update \
    && apt -y install libmecab-dev

ADD ./lib/analyzer /app

RUN cargo build --release



FROM python:3.11

WORKDIR /app

RUN apt update \
    && apt -y install mecab libmecab-dev

COPY --from=0 /app/target/release/analyzer /bin/analyzer
COPY /app/src /app/src

RUN pip install --upgrade pip \
    && pip install flask==2.3.2 line-bot-sdk==2.4.2 Flask-SQLAlchemy==3.0.5 Flask-APScheduler==1.12.4 gunicorn==20.1.0

ENV PYTHONPATH $PYTHONPATH:/app/src

CMD gunicorn -w 4 -b 0.0.0.0:5000 'src.server:create_prod_app()'
