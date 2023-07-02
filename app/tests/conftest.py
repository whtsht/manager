from server import Mode, create_app
from info import db, Plan
from plan.notify import sched
import pytest


@pytest.fixture(scope="session")
def app():
    app = create_app(Mode.Dev)
    app.app_context().push()

    yield app

    db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def clean_up():
    yield db.session

    db.session.query(Plan).delete()
    db.session.commit()

    jobs = sched.get_jobs()
    for job in jobs:
        job.remove()
