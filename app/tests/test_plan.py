from plan.main import main
from info import Plan
from plan.notify import sched
from datetime import datetime, timezone, timedelta

mockLineID = "xjoqwejadfldskhfawe12"
mockLineID2 = "xjoqwejadfldskhfawe12_2"
tzinfo = timezone(timedelta(hours=9))


def test_add_plan(client):
    main("2099/08/01の9:00から学校", mockLineID)
    main("2099/08/01の9:00から学校", mockLineID2)

    plans = Plan.query.all()
    assert len(plans) == 2
    assert plans[0].title == "学校"
    assert plans[0].line_id == mockLineID

    jobs = sched.get_jobs()
    assert len(jobs) == 2

    assert jobs[0].trigger.run_date == datetime(2099, 8, 1, 9, 0, tzinfo=tzinfo)


def add_test_err(client):
    main("2099/08/01の9:00から学校", mockLineID)
    result = main("2099/08/01の9:00から学校", mockLineID)
    assert result == "その予定は既に追加されています"


def test_search_plan(client):
    main("2099/03/03の9:00から学校", mockLineID)
    main("2099/03/03の16:00から遊び", mockLineID)

    result = main("予定検索 学校", mockLineID)
    assert result == "予定が見つかりました。\nタイトル: 学校\n開始時刻: 2099-03-03 09:00:00"

    result = main("予定検索 遊び", mockLineID)
    assert result == "予定が見つかりました。\nタイトル: 遊び\n開始時刻: 2099-03-03 16:00:00"

    result = main("予定検索 学校 2099/03/03", mockLineID)
    assert result == "予定が見つかりました。\nタイトル: 学校\n開始時刻: 2099-03-03 09:00:00"

    result = main("予定検索 遊び 2099/03/03", mockLineID)
    assert result == "予定が見つかりました。\nタイトル: 遊び\n開始時刻: 2099-03-03 16:00:00"

    result = main("予定検索 2099/03/03", mockLineID)
    assert (
        result
        == "予定が見つかりました。\nタイトル: 学校\n開始時刻: 2099-03-03 09:00:00\n\nタイトル: 遊び\n開始時刻: 2099-03-03 16:00:00"
    )

    result = main("予定検索 遊び 2099/03/04", mockLineID)
    assert result == "予定を見つけることができませんでした。"


def test_search_err(client):
    result = main("検索", mockLineID)
    assert result == "予定のタイトル、日付のどちらかを入力して下さい。"
