from server import Mode, create_app
from info import db, Plan
import json
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


def test_modify_plan(client):
    client.post(
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

    plans = Plan.query.all()
    client.post(
        "/web/modify_plan/",
        json={
            "plan": {
                "id": plans[0].id,
                "title": "タイトル2",
                "detail": "詳細2",
                "lineID": mockLineID,
                "notifTime": "2023/03/03T13:33",
                "allDay": None,
                "start": "2023/03/03T13:33",
                "end": "2023/03/03T13:33",
            },
        },
    )

    plans = Plan.query.all()
    assert len(plans) == 1
    assert plans[0].title == "タイトル2"
    assert plans[0].allday == None


def test_remove_plan(client):
    client.post(
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

    plans = Plan.query.all()
    client.post(
        "/web/remove_plan/",
        json={
            "planID": plans[0].id,
        },
    )

    plans = Plan.query.all()
    assert len(plans) == 0


def test_get_plan_list(client):
    client.post(
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
    client.post(
        "/web/add_plan/",
        json={
            "plan": {
                "title": "タイトル2",
                "detail": "詳細2",
                "lineID": mockLineID,
                "notifTime": "2023/03/03T13:33",
                "allDay": None,
                "start": "2023/03/03T13:33",
                "end": "2023/03/03T13:33",
            },
        },
    )

    response = client.post(
        "/web/get_plan_list/",
        json={
            "lineID": mockLineID,
        },
    )

    data = json.loads(response.data)
    assert "タイトル" == data[0]["title"]
    assert "タイトル2" == data[1]["title"]
