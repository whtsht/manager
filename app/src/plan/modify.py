from web import web
from flask import request
from db_models import Plan, db


@web.route("/modify_plan/", methods=["POST"])
def modify_plan():
    if data := request.json:
        plan_id: str = data["planID"]
        plan: Plan = data["plan"]
        db_plan: Plan = Plan.query.filter_by(Plan.id == plan_id).first()
        db_plan.title = plan.title
        db_plan.detail = plan.detail
        db_plan.notif_time = plan.notif_time
        db_plan.allday = plan.allday
        db_plan.start_time = plan.start_time
        db_plan.end_time = plan.end_time
        db.session.commit()

    return "ok"
