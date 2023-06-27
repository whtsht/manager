"""
Designer:   石川隼
Date:       2023/06/24
Purpose:    予定の削除処理
"""

from info import PlanInfo,Plan, db
from web import web
from flask import request



def remove_plan(plan_id: str):
    """M29 予定削除処理　予定をデータベースから削除
    Args: 
        str (plan_id): 予定のid
    """
    plan = db.session.query(Plan).filter(Plan.plan_id == plan_id).first()
    db.session.delete(plan)
    db.session.commit()





