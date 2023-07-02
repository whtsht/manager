from plan.main import main
from info import Plan
from plan.notify import sched


mockLineID = "xjoqwejadfldskhfawe12"


def test_add_plan(client):
    main("2023/08/01の9:00から学校", mockLineID)

    plans = Plan.query.all()
    assert len(plans) == 1
    assert plans[0].title == "学校"
    assert plans[0].line_id == mockLineID

    jobs = sched.get_jobs()
    assert len(jobs) == 1


def test_search_plan(client):
    main("2023/03/03の9:00から学校", mockLineID)
    result = main("予定検索 学校", mockLineID)

    assert result == "予定が見つかりました。\nタイトル: 学校\n開始時刻: 2023-03-03 09:00:00"
