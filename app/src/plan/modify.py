"""
Designer:   石川隼
Date:       2023/06/24
Purpose:    予定修正に関する関数
"""

from info import Plan, db


def modify_plan(_: int, plan: Plan):
    """M30 予定修正処理

    Args:
        plan_id (int): 予定情報
        plan (Plan): 予定
    """
    db_plan: Plan = Plan.query.filter_by(Plan.id == plan.id).first()
    db_plan.title = plan.title
    db_plan.detail = plan.detail
    db_plan.notif_time = plan.notif_time
    db_plan.allday = plan.allday
    db_plan.start_time = plan.start_time
    db_plan.end_time = plan.end_time
    db.session.commit()
