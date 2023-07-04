"""
Dedigner: 菊地智遥
Date: 2023/6/20
Purpose: 
"""

from typing import Optional, cast
from plan.notify import NotifPlan, add_notification
from info import (
    PlanInfo,
    AddError,
    StrictDateTime,
    db,
    Plan,
    new_plan,
    get_start_time,
)
from datetime import datetime, timedelta


def from_message(line_id: str, plan_info: PlanInfo) -> Optional[AddError]:
    """予定情報に不足がないか確認、通知時間を開始時刻の30分前に設定してM22を実行してNoneを返す。

    Args:
        lineID (str):lineID
        plan_info (PlanInfo): 予定情報

    Returns:
        Optional[AddErrorType]: 予定が追加できたか
    """
    if plan_info.title is None:
        return AddError.TitleNotSet
    elif (
        plan_info.start_time.date.year is None
        or plan_info.start_time.date.month is None
        or plan_info.start_time.date.day is None
        or plan_info.start_time.time.hour is None
    ):
        return AddError.DateTimeNotSet
    elif (plan_info.start_time.time.hour is None):
        return AddError.TimeNotSet
    elif (
        plan_info.start_time.date.month is None
        or plan_info.start_time.date.day is None
    ):
        return AddError.DateNotSet
    else:
        start_time = StrictDateTime(
            int(plan_info.start_time.date.year),
            int(plan_info.start_time.date.month),
            int(plan_info.start_time.date.day),
            int(plan_info.start_time.time.hour),
            plan_info.start_time.time.minute,
        )
        if (
            Plan.query.filter(Plan.line_id == line_id)
            .filter(Plan.title == plan_info.title)
            .filter(get_start_time(Plan) == start_time.into())
            .first()
            is not None
        ):
            return AddError.AlreadyExist
        else:
            notif_time = start_time.into()
            if (datetime.now() + timedelta(minutes=30)) < notif_time:
                notif_time -= timedelta(minutes=30)
            notif_time = StrictDateTime(
                notif_time.year,
                notif_time.month,
                notif_time.day,
                notif_time.hour,
                notif_time.minute,
            )
            plan = new_plan(plan_info.title, line_id, notif_time, start_time)
            add_plan(plan)
            # 予定追加成功
            return None


def add_plan(plan: Plan):
    """DBに予定を追加する
    Args:
        plan: 予定の情報
        line_id: Line ID
    """
    # 通知設定

    add_notification(
        NotifPlan(
            plan.line_id,
            plan.title,
            cast(datetime, plan.allday or plan.start_time),
            plan.notif_time,
        )
    )
    db.session.add(plan)
    db.session.commit()


def uncompleted_message(error: AddError) -> str:
    """エラーメッセージを作成する
    Args: error: どのタイプのエラーか
    Returns: エラーメッセージ"""
    if error == AddError.AlreadyExist:
        return "その予定は既に追加されています"
    if error == AddError.TitleNotSet:
        return "タイトルが設定されていません"
    if error == AddError.TimeNotSet:
        return "開始時刻が設定されていません"
    if error == AddError.DateNotSet:
        return "開始日時が設定されていません"
    return "month/day/timeに「title」と入力して下さい"


def complited_message(plan_info: PlanInfo) -> str:
    """完了メッセージを作成する

    Args:
        plan_info (PlanInfo): 予定情報

    Returns:
        mes (str): 完了メッセージ
    """
    mes = (
        "予定の追加が完了しました。"
        + f"タイトルは{plan_info.title}、"
        + f"開始時間は{plan_info.start_time.date.month}/{plan_info.start_time.date.day}"
        + f" {plan_info.start_time.time.hour}:{plan_info.start_time.time.minute}"
        + "です。"
    )

    return mes
