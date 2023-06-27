"""
Designer:   石川隼
Date:       2023/06/24
Purpose:    予定修正に関する関数
"""

from web import web
from flask import request
from info import Plan, db


def modify_plan(plan_id:int, plan:Plan):
    """M30 予定修正処理

    Args:
        plan_id (int): 予定情報
        plan (Plan): 予定
    """
    if data := request.json:
        PLAN: Plan = data["plan"]
        db_PLAN: Plan = Plan.query.filter_by(Plan.id == plan.id).first()
        db_PLAN.title = plan.title
        db_PLAN.detail = plan.detail
        db_PLAN.notif_time = plan.notif_time
        db_PLAN.allday = plan.allday
        db_PLAN.start_time = plan.start_time
        db_PLAN.end_time = plan.end_time
        db.session.commit()
