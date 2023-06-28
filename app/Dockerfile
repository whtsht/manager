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
    && pip install flask line-bot-sdk Flask-SQLAlchemy Flask-APScheduler gunicorn

ENV PYTHONPATH $PYTHONPATH:/app/src

CMD gunicorn -w 4 -b 0.0.0.0:5000 'src.server:create_prod_app()'
