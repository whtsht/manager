"""
Dedigner: 菊地智遥
Date: 2023/6/20
Purpose: 
"""

from typing import Optional
from info import (
    PlanInfo,
    AddError,
    StrictDateTime,
    db,
    Plan,
    new_plan,
    AddErrorType,
    get_start_time,
)
from datetime import timedelta


def from_message(lineID: str, plan_info: PlanInfo) -> Optional[AddErrorType]:
    """予定情報に不足がないか確認、通知時間を開始時刻の30分前に設定してM22を実行してNoneを返す。

    Args:
        lineID (str):lineID
        plan_info (PlanInfo): 予定情報

    Returns:
        Optional[AddErrorType]: 予定が追加できたか
    """
    if plan_info.title is None:
        return AddErrorType.TitleNotSet
    elif (
        plan_info.start_time.date.year is None
        or plan_info.start_time.date.month is None
        or plan_info.start_time.date.day is None
        or plan_info.start_time.time.hour is None
    ):
        return AddErrorType.TimeNotSet
    else:
        start_time = StrictDateTime(
            int(plan_info.start_time.date.year),
            int(plan_info.start_time.date.month),
            int(plan_info.start_time.date.day),
            int(plan_info.start_time.time.hour),
            plan_info.start_time.time.minute,
        )
        if (
            db.session.query(Plan).filter(Plan.title == plan_info.title).first() is None  # type: ignore
            or db.session.query(Plan)
            .filter(get_start_time(Plan) == start_time.into())  # type: ignore
            .first()
            is None
        ):
            notif_time = start_time.into()
            notif_time -= timedelta(minutes=30)
            notif_time = StrictDateTime(
                notif_time.year,
                notif_time.month,
                notif_time.day,
                notif_time.hour,
                notif_time.minute,
            )
            plan = new_plan(plan_info.title, lineID, notif_time, start_time)
            add_plan(plan)
            # 予定追加成功
            return None
        else:
            return AddErrorType.AlreadyExist


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
    if error.error_type == AddErrorType.AlreadyExist:
        return "その予定は既に追加されています"
    if error.error_type == AddErrorType.TitleNotSet:
        return "タイトルが設定されていません"
    if error.error_type == AddErrorType.TimeNotSet:
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
