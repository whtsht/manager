"""
Designer: 小田桐光佑, 東間日向
Date: 2023/6/27
Purpose:通知処理を行う関数
"""
from flask_apscheduler import APScheduler
from datetime import datetime
from linebot import LineBotApi
from info import Plan, get_start_time
from secret import CHANNEL_ACCESS_TOKEN
from datetime import timedelta, datetime
from typing import cast
from linebot.models import (
    ButtonsTemplate,
    TextSendMessage,
    MessageAction,
    TemplateSendMessage,
)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

sched = APScheduler()


class NotifPlan:
    """通知する予定を保持する
    Planをそのまま保持すると，send_notificationを呼び出したとき，
    SQLのセッション切れによってエラーがでる．それを回避するためのクラス
    """

    def __init__(
        self, line_id: str, title: str, start_time: datetime, notif_time: datetime
    ):
        self.line_id = line_id
        self.title = title
        self.start_time = start_time
        self.notif_time = notif_time


def gen_id(line_id: str, title: str, date: datetime) -> str:
    """ジョブに対して唯一のIDを生成する:M20

    Args:
        line_id (str): lineID
        title (str): タイトル
        date (datetime): 日付
    Returns:
        line_id + "_" + title + "_" + str(date)
    """
    return line_id + "_" + title + "_" + str(date)


def from_plan(plan: Plan) -> NotifPlan:
    return NotifPlan(
        plan.line_id,
        plan.title,
        cast(datetime, plan.allday or plan.start_time),
        plan.notif_time,
    )


def add_notification(plan: NotifPlan):
    """予定通知処理をジョブリストに追加:M21
        start_timeかalldayのどちらか必ず値が入っている

    Args:
        plan (NofifPlan): 予定
    """
    sched.add_job(
        gen_id(plan.line_id, plan.title, plan.start_time),
        send_notification,
        trigger="date",
        run_date=plan.notif_time,
        args=[NotifPlan(plan.line_id, plan.title, plan.start_time, plan.notif_time)],
    )


def cancel_notification(plan: Plan):
    """ジョブリストから通知処理通知を削除:M22

    Args:
        plan: (Plan): 予定
    """
    start_time = cast(datetime, plan.start_time or plan.allday)
    sched.remove_job(
        gen_id(plan.line_id, plan.title, start_time),
    )


def snooze(line_id: str, after: int) -> str:
    """利用者がスヌーズを押した場合,latest_planから最新の予定を取得し,5/10/30/分後に通知する
         その予定の開始時刻から30分以上経過している場合は,予定が古すぎることを知らせる:M23

    Args:
        line_id (str): lineID
        after (int): after分後に通知
    """
    now = datetime.utcnow() + timedelta(hours=9)
    plans: list[Plan] = Plan.query.filter(Plan.line_id == line_id).all()
    plans = list(
        filter(
            lambda plan: get_start_time(plan).date() == now.date(),
            plans,
        )
    )
    if len(plans) == 0:
        return "該当する予定が見つかりません。"
    else:
        # TODO
        # 現在時刻に最も近い予定を取得する
        plan: Plan = plans[0]

        ids = list(map(lambda job: job.id, sched.get_jobs()))
        start_time = cast(datetime, plan.start_time or plan.allday)
        if gen_id(plan.line_id, plan.title, start_time) in ids:
            return f"既に設定されています"
        else:
            n_plan: NotifPlan = from_plan(plan)
            n_plan.notif_time = now + timedelta(minutes=after)
            add_notification(n_plan)
            return f"{after}分後にスヌーズします"


def send_notification(plan: NotifPlan):
    """利用者に予定の通知を行う:M24

    Args:
        plan (NotifPlan): プラン
    """
    line_id = plan.line_id
    push_buttons_message(
        line_id,
        plan.title + "の時間です",
        "何分後にスヌーズを設定するのか押してください",
        ["5分 スヌーズ", "10分 スヌーズ", "15分 スヌーズ"],
    )


def push_text_message(line_id: str, message: str):
    """利用者のLineにメッセージを送信する

    Args:
        line_id (str): Line ID
        message (str): メッセージ
    """
    line_bot_api.push_message(line_id, TextSendMessage(message))


def push_buttons_message(line_id: str, title: str, message: str, buttons: list[str]):
    """利用者にメッセージとボタンを送信する

    Args:
        line_id (str): Line ID
        title (str): タイトル
        message (str): メッセージ
        buttons (list[str]): ボタンに表示するメッセージ
    """
    buttons_template_message = TemplateSendMessage(
        alt_text=title,
        template=ButtonsTemplate(
            title=" " if len(title) == 0 else title,
            text=" " if len(message) == 0 else message,
            actions=map(
                lambda button: MessageAction(label=button, text=button), buttons
            ),
        ),
    )
    line_bot_api.push_message(line_id, buttons_template_message)
