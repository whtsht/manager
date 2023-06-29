from plan.main import main
from server import Mode, create_app
from info import db, Plan
from plan.notify import sched
import pytest

mockLineID = "xjoqwejadfldskhfawe12"


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

    # スケジュールを全て削除
    jobs = sched.get_jobs()
    for job in jobs:
        job.remove()


@pytest.fixture()
def client(app):
    return app.test_client()


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
