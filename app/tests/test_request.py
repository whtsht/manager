from info import Plan
from plan.notify import sched
import json


mockLineID = "xjoqwejadfldskhfawe12"


def test_add_plan(client):
    result = client.post(
        "/web/add_plan/",
        json={
            "plan": {
                "title": "タイトル",
                "detail": "詳細",
                "lineID": mockLineID,
                "notifTime": "2099/03/03T13:33",
                "allDay": "2099/03/03T13:33",
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

    jobs = sched.get_jobs()
    assert len(jobs) == 1


def test_modify_plan(client):
    client.post(
        "/web/add_plan/",
        json={
            "plan": {
                "title": "タイトル",
                "detail": "詳細",
                "lineID": mockLineID,
                "notifTime": "2099/03/03T13:33",
                "allDay": "2099/03/03T13:33",
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
                "notifTime": "2099/03/03T13:33",
                "allDay": None,
                "start": "2099/03/03T13:33",
                "end": "2099/03/03T13:33",
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
                "notifTime": "2099/03/03T13:33",
                "allDay": "2099/03/03T13:33",
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

    jobs = sched.get_jobs()
    assert len(jobs) == 0


def test_get_plan_list(client):
    client.post(
        "/web/add_plan/",
        json={
            "plan": {
                "title": "タイトル",
                "detail": "詳細",
                "lineID": mockLineID,
                "notifTime": "2099/03/03T13:33",
                "allDay": "2099/03/03T13:33",
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
                "notifTime": "2099/03/03T13:33",
                "allDay": None,
                "start": "2099/03/03T13:33",
                "end": "2099/03/03T13:33",
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
