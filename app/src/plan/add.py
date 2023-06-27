"""
Dedigner: 菊地智遥
Date: 2023/6/20
Purpose: 
"""

from db_models import db, Plan
from info import PlanInfo, AddError


def from_message(lineID: str, plan_info: PlanInfo):
    pass


def add_plan(plan: Plan):
    """DBに予定を追加する
    Args: plan: 予定の情報
    Returns: なし
    """
    db.session.add(plan)
    db.session.commit()


def uncompleted_message(error: AddError):
    """エラーメッセージを作成する
    Args: error: どのタイプのエラーか
    Returns: エラーメッセージ"""
    if error.error_type == 1:
        return "その予定は既に追加されています"
    if error.error_type == 2:
        return "タイトルが設定されていません"
    if error.error_type == 3:
        return "開始時間が設定されていません"


def complited_message(plan_info: PlanInfo):
    """完了メッセージを作成する

    Args:
        plan_info (PlanInfo): 予定情報

    Returns:
        mes (str): 完了メッセージ
    """
    mes = f"予定の追加が完了しました。タイトルは{plan_info.title}、開始時間は{plan_info.start_time}です。"

    return mes
