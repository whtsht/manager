"""
Designer:   石川隼
Date:       2023/06/24
Purpose:    予定修正に関する関数
"""

from web import web
from flask import request
from db_models import Plan, db


@web.route("/modify_plan/", methods=["POST"])
def modify_plan():
    """M30 予定修正処理
    """
    if data := request.json:
        plan: Plan = data["plan"]
        db_plan: Plan = Plan.query.filter_by(Plan.id == plan.id).first()
        db_plan.title = plan.title
        db_plan.detail = plan.detail
        db_plan.notif_time = plan.notif_time
        db_plan.allday = plan.allday
        db_plan.start_time = plan.start_time
        db_plan.end_time = plan.end_time
        db.session.commit()

    return "ok"
