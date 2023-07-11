from plan.main import main
from info import Plan
from plan.notify import sched
from datetime import datetime, timezone, timedelta

mockLineID = "xjoqwejadfldskhfawe12"
mockLineID2 = "xjoqwejadfldskhfawe12_2"
tzinfo = timezone(timedelta(hours=9))


def test_add_plan(client):
    result = main("追加 2099/08/01の9:00 学校", mockLineID)
    assert result == "予定の追加が完了しました。タイトルは学校、開始時間は2099/08/01 - 09:00です。"
    main("追加 2099/08/01の9:00 学校", mockLineID2)

    plans = Plan.query.all()
    assert len(plans) == 2
    assert plans[0].title == "学校"
    assert plans[0].line_id == mockLineID

    jobs = sched.get_jobs()
    assert len(jobs) == 2

    # 30分前に通知
    assert jobs[0].trigger.run_date == datetime(2099, 8, 1, 8, 30, tzinfo=tzinfo)

    ptime = datetime.now(tz=tzinfo) + timedelta(minutes=15)

    main("追加 " + ptime.strftime("%Y/%m/%d %H:%M") + " 学校", mockLineID2)
    plans = Plan.query.all()
    assert len(plans) == 3

    jobs = sched.get_jobs()
    assert len(jobs) == 3

    # 0分前に通知
    assert jobs[0].trigger.run_date == datetime(
        ptime.year, ptime.month, ptime.day, ptime.hour, ptime.minute, tzinfo=tzinfo
    )


def add_test_err(client):
    main("追加 2099/08/01の9:00 学校", mockLineID)
    result = main("追加 2099/08/01の9:00 学校", mockLineID)
    assert result == "その予定は既に追加されています"


#
#
def test_search_plan(client):
    main("追加 2099/03/03 9:00 学校", mockLineID)
    main("追加 2099/03/03 16:00 遊び", mockLineID)

    main("追加 2099/03/03の9:00 学校", mockLineID2)
    main("追加 2099/03/03の16:00 遊び", mockLineID2)

    result = main("予定検索 学校", mockLineID)
    assert result == "予定が見つかりました。\nタイトル: 学校\n開始時刻: 2099/03/03 - 09:00"

    result = main("予定検索 遊び", mockLineID)
    assert result == "予定が見つかりました。\nタイトル: 遊び\n開始時刻: 2099/03/03 - 16:00"

    result = main("予定検索 学校 2099/03/03", mockLineID)
    assert result == "予定が見つかりました。\nタイトル: 学校\n開始時刻: 2099/03/03 - 09:00"

    result = main("予定検索 遊び 2099/03/03", mockLineID)
    assert result == "予定が見つかりました。\nタイトル: 遊び\n開始時刻: 2099/03/03 - 16:00"

    result = main("予定検索 2099/03/03", mockLineID)
    assert (
        result
        == "予定が見つかりました。\nタイトル: 学校\n開始時刻: 2099/03/03 - 09:00\n\nタイトル: 遊び\n開始時刻: 2099/03/03 - 16:00"
    )

    result = main("予定検索 遊び 2099/03/04", mockLineID)
    assert result == "予定を見つけることができませんでした。"


# def test_search_err(client):
#     result = main("検索", mockLineID)
#     assert result == "予定のタイトル、日付のどちらかを入力して下さい。"
