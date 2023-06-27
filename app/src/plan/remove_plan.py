"""
Designer:   石川隼
Date:       2023/06/24
Purpose:    予定の削除処理
"""

from info import Plan, db


def remove_plan(plan_id: str):
    """M29 予定削除処理"""
    plan = db.session.query(Plan).filter(Plan.plan_id == plan_id).first()
    db.session.delete(plan)
    db.session.commit()
