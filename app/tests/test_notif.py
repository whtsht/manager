from plan.notify import sched, add_notification, NotifPlan
from datetime import datetime


def test_add_notif(client):
    add_notification(
        NotifPlan(
            "id",
            "title",
            datetime(2010, 10, 10, 10, 10),
            datetime(2010, 10, 10, 10, 10),
        )
    )

    jobs = sched.get_jobs()
    assert len(jobs) == 1
    print(jobs[0].__slots__)
