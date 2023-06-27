from server import Mode, create_app
from info import db, Plan
import pytest


@pytest.fixture(scope="session")
def app():
    app = create_app(Mode.Dev)
    app.app_context().push()

    yield app

    db.drop_all()


# 1テスト毎に実行
@pytest.fixture(scope="function", autouse=True)
def session():
    yield db.session

    # テーブル内のデータを全て削除
    db.session.query(Plan).delete()
    db.session.commit()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_hello(client):
    result = client.get("/web/hello/")
    assert b"hello :)" == result.data


def test_add_plan(client):
    result = client.post("/web/add_plan/", json={})
    assert b""
