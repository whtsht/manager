"""
Designer:   東間日向
Date:       2023/06/17
Purpose:    データベースに保存するクラスの定義
"""
from flask_sqlalchemy import SQLAlchemy
from info import StrictDateTime
from typing import Optional
from datetime import datetime

# データベースのインスタンス
db = SQLAlchemy()


class Plan(db.Model):
    """F1 予定情報を格納する
    Attributes:
        id: 予定ID
        line_id: LineID
        title: 予定名
        detail: 詳細
        notif_time: 通知時刻
        allday: 終日
        start_time: 開始時刻
        end_time: 終了時刻
    """

    __tablename__ = "plans"
    id: int = db.Column(db.Integer, primary_key=True)
    line_id: str = db.Column(db.String(50), nullable=False)
    title: str = db.Column(db.String(100), nullable=False)
    detail: Optional[str] = db.Column(db.String(300), nullable=False)
    notif_time: datetime = db.Column(db.DateTime, nullable=False)
    allday: Optional[datetime] = db.Column(db.DateTime, nullable=True)
    start_time: Optional[datetime] = db.Column(db.DateTime, nullable=True)
    end_time: Optional[datetime] = db.Column(db.DateTime, nullable=True)

    def __init__(
        self,
        title: str,
        line_id: str,
        detail: Optional[str],
        notif_time: StrictDateTime,
        allday: Optional[StrictDateTime],
        start_time: Optional[StrictDateTime],
        end_time: Optional[StrictDateTime],
    ):
        """予定情報
        Args:
            title (str):
                予定名
            line_id (str):
                LineID
            detail (Optional[str]):
                詳細
            notif_time (StrictDateTime):
                通知時間
            allday (Optional[StrictDateTime]):
                終日
            start_time (Optional[StrictDateTime]):
                開始時刻
            end_time (Optional[StrictDateTime]):
                終了時刻
        """
        self.line_id = line_id
        self.title = title
        self.detail = detail
        self.notif_time = notif_time.into()
        self.allday = into_datatime(allday)
        self.start_time = into_datatime(start_time)
        self.end_time = into_datatime(end_time)


def into_datatime(time: Optional[StrictDateTime]) -> Optional[datetime]:
    return None if time == None else time.into()


def new_plan(
    title: str, line_id: str, notif_time: StrictDateTime, start_time: StrictDateTime
) -> Plan:
    """シンプルな予定生成関数

    Args:
        title (str):
            予定名
        line_id (str):
            LineID
        notif_time (StrictDateTime):
            通知時刻
        start_time (StrictDateTime):
            開始時刻

    Returns:
        Plan: 予定情報
    """
    return Plan(title, line_id, None, notif_time, None, start_time, None)
