"""
Dedigner: 小田桐光佑, 東間日向
Date: 2023/6/27
Purpose:通知処理を行う関数
"""
from flask import current_app
from flask_apscheduler import APScheduler
from datetime import datetime
from linebot import LineBotApi
from info import Plan
from src.secret import CHANNEL_ACCESS_TOKEN
from datetime import timedelta, datetime
from linebot.models import (
    ButtonsTemplate,
    TextSendMessage,
    MessageAction,
    TemplateSendMessage,
)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

sched = APScheduler()


class NotifPlan:
    def __init__(
        self, line_id: str, title: str, start_time: datetime, notif_time: datetime
    ):
        self.line_id = line_id
        self.title = title
        self.start_time = start_time
        self.notif_time = notif_time


# lineID => 予定を検索
latest_plan: dict[str, NotifPlan] = {}


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


def add_notification(plan: NotifPlan):
    """予定通知処理をジョブリストに追加:M21
        start_timeかalldayのどちらか必ず値が入っている

    Args:
        line_id (str): lineID
        plan (Plan): プラン
    """
    global latest_plan
    line_id = plan.line_id

    # 予定を記録
    latest_plan[line_id] = plan

    start_time = plan.start_time
    # 30分前
    sched.add_job(
        gen_id(line_id, plan.title, start_time),  # type: ignore
        send_notification,
        trigger="date",
        run_date=plan.notif_time,
        args=[plan],
    )
    # 0分前
    sched.add_job(
        gen_id("_" + line_id, plan.title, start_time),  # type: ignore
        send_notification,
        trigger="date",
        run_date=start_time,
        args=[plan],
    )
    current_app.logger.info(f"Add Task {plan.title}")  # type: ignore


def cancel_notification(plan: Plan):
    """ジョブリストから通知処理通知を削除:M22

    Args:
        line_id (str): lineID
        title (str): タイトル
        date (datetime): 日付
    """
    global latest_plan
    line_id = plan.line_id
    if line_id in latest_plan.keys():
        del latest_plan[line_id]

    start_time = plan.start_time or plan.allday
    sched.remove_job(
        gen_id(plan.line_id, plan.title, start_time),  # type: ignore
    )


def snooze(line_id: str, after: int) -> str:
    """利用者がスヌーズを押した場合,latest_planから最新の予定を取得し,5/10/30/分後に通知する
         その予定の開始時刻から30分以上経過している場合は,予定が古すぎることを知らせる:M23

    Args:
        line_id (str): lineID
        after (int): after分後に通知
    """
    global latest_plan

    if line_id in latest_plan.keys():
        plan = latest_plan[line_id]
        start_time = plan.start_time
        current_time = datetime.now()
        snooze_time = current_time + timedelta(minutes=after)

        if snooze_time < start_time:  # type: ignore
            plan.notif_time = snooze_time
            add_notification(plan)
            # push_text_message(line_id, "スヌーズします")
            return "スヌーズします"
        else:
            # push_text_message(line_id, "予定が古すぎます。")
            return "予定が古すぎます。"
    else:
        # push_text_message(line_id, "該当する予定が見つかりません。")
        return "該当する予定が見つかりません。"


def send_notification(plan: NotifPlan):
    """利用者に予定の通知を行う:M24

    Args:
        line_id (str): lineID
        plan (Plan): プラン
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
