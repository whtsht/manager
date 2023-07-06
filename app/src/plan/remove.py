"""
Designer:   石川隼
Date:       2023/06/24
Purpose:    予定の削除処理
"""

from info import Plan, db
from plan.notify import cancel_notification


def remove_plan(plan_id: str):
    """M29 予定削除処理 予定をデータベースから削除
    Args:
        str (plan_id): 予定のid
    """

    plan = Plan.query.filter(Plan.id == int(plan_id)).first()
    try:
        # 通知が未設定な場合は何もしない
        cancel_notification(plan)
    except:
        pass
    db.session.delete(plan)
    db.session.commit()
