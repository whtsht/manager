"""
Designer:   東間日向
Date:       2023/06/20
Purpose:    予定修正に関する関数
"""

from web import web
from flask import request
from db_models import Plan, db


@web.route("/modify_plan/", methods=["POST"])
def modify_plan():
    """M36 予定修正処理
    M3の要求を受け，予定を修正する．データベースからPlanのidと一致する予定を見つけ，それを更新する．
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
