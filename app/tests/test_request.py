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


mockLineID = "xjoqwejadfldskhfawe12"


def test_add_plan(client):
    result = client.post(
        "/web/add_plan/",
        json={
            "plan": {
                "title": "タイトル",
                "detail": "詳細",
                "lineID": mockLineID,
                "notifTime": "2023/03/03T13:33",
                "allDay": "2023/03/03T13:33",
                "start": None,
                "end": None,
            },
        },
    )

    assert b"ok" == result.data

    plans = Plan.query.all()
    assert len(plans) == 1
    assert plans[0].title == "タイトル"
    assert plans[0].notif_time.hour == 13
