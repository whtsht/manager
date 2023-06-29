"""
Designer:   東間日向
Date:       2023/06/18
Purpose:    サーバーの初期設定
"""
from flask import Flask
from enum import Enum
from web import web
from info import db
from line import line
from plan.notify import sched
import logging


class Mode(Enum):
    Prod = (1,)
    Dev = (2,)


def create_app(mode: Mode):
    app = Flask(__name__)
    if mode == Mode.Dev:
        logging.basicConfig(level=logging.INFO)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    else:
        # logging.basicConfig(level=logging.ERROR)
        logging.basicConfig(level=logging.INFO)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////app/data.db"

    app.register_blueprint(web)
    app.register_blueprint(line)
    with app.app_context():
        db.init_app(app)
        try:
            db.create_all()
        except:
            pass

    app.config["SCHEDULER_TIMEZONE"] = "Asia/Tokyo"
    sched.init_app(app)
    sched.start()

    return app


def create_prod_app():
    return create_app(Mode.Prod)


def create_dev_app():
    return create_app(Mode.Dev)
