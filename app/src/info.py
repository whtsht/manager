"""
Designer:   東間日向
Date:       2023/06/17
Purpose:    他モジュールで使うクラスの定義
"""
from typing import Optional
from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from typing import Optional
from datetime import datetime


class Date:
    def __init__(self, year: Optional[int], month: Optional[int], day: Optional[int]):
        self.year = year
        self.month = month
        self.day = day


class Time:
    def __init__(self, hour: Optional[int], minute: Optional[int]):
        self.hour = hour
        self.minute = minute


class DateTime:
    """曖昧な時刻情報を格納する

    例)
        各要素が入っていない可能性がある
        2023/05/15 XX:XX
        XXXX/XX/XX XX:XX
        XXXX/11/11 09:XX
    """

    def __init__(self, date: Date, time: Time):
        self.date = date
        self.time = time

    def into(self) -> datetime | None:
        if (
            self.date.year is not None
            and self.date.month is not None
            and self.date.day is not None
        ):
            return datetime(
                self.date.year,
                self.date.month,
                self.date.day,
                self.time.hour or 0,
                self.time.minute or 0,
            )


class StrictDateTime:
    """厳密な時刻情報を格納する

    例)
        分以外は指定する必要がある
        2023/05/15 14:30
        2023/11/11 09:XX
    """

    def __init__(
        self, year: int, month: int, day: int, hour: int, minute: Optional[int] = None
    ):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def into(self) -> datetime:
        """データベースに格納できるように値を変換

        Returns:
            datetime
        """
        return datetime(self.year, self.month, self.day, self.hour, self.minute or 0)


# データベースのインスタンス
db = SQLAlchemy()


class Plan(db.Model):
    """F1 予定情報
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
        notif_time: datetime,
        allday: Optional[datetime],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        id: Optional[int] = None,
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
        if id:
            self.id = id
        self.line_id = line_id
        self.title = title
        self.detail = detail or ""
        self.notif_time = notif_time
        self.allday = allday
        self.start_time = start_time
        self.end_time = end_time


def get_start_time(plan: Plan) -> datetime:
    return plan.allday or plan.start_time  # type: ignore


class OP(Enum):
    """操作
    Add:
        追加
    Search:
        検索
    """

    Add = (1,)
    Search = (2,)


class PlanInfo:
    """予定情報
    Attributes:
        title (Optional[str]):
            予定名
        start_time (DateTime):
            開始時刻
    """

    def __init__(self, title: Optional[str], start_time: DateTime):
        self.title = title
        self.start_time = start_time


class InputInfo:
    """入力情報
    Attributes:
        title (str):
            予定名
        op (OP):
            操作
        start_time (DateTime):
            開始時刻

    """

    def __init__(
        self,
        title: Optional[str],
        operation: Optional[OP],
        start_time: DateTime,
    ) -> None:
        self.title = title
        self.op = operation
        self.start_time = start_time

    def into_plan_info(self) -> PlanInfo:
        """入力情報から予定情報への変換

        Returns:
            PlanInfo: 予定情報
        """
        return PlanInfo(self.title, self.start_time)


class AddError(Enum):
    """追加処理エラー"""

    AlreadyExist = 1
    TitleNotSet = 2
    TimeNotSet = 3
    DateNotSet = 4
    DateTimeNotSet = 5


class SearchError(Enum):
    """検索処理のエラー"""

    NotFound = 1
    LackInfo = 2


class UserState(db.Model):
    """F2 利用者状態
    Attributes:
        line_id: LineID
        op: 操作名
        completed: 操作完了
        title: 予定名
        start_time: 開始時刻
        add_error: 予定追加エラー
        search_error: 予定検索エラー
    """

    line_id: str = db.Column(db.String(50), primary_key=True)
    op: str = db.Column(db.String(20), nullable=False)
    completed: bool = db.Column(db.Boolean, nullable=False)
    title: Optional[str] = db.Column(db.String(100), nullable=True)
    year: Optional[int] = db.Column(db.Integer, nullable=True)
    month: Optional[int] = db.Column(db.Integer, nullable=True)
    day: Optional[int] = db.Column(db.Integer, nullable=True)
    hour: Optional[int] = db.Column(db.Integer, nullable=True)
    minute: Optional[int] = db.Column(db.Integer, nullable=True)
    add_error: Optional[str] = db.Column(db.String(20), nullable=True)
    search_error: Optional[str] = db.Column(db.String(20), nullable=True)

    def __init__(
        self,
        line_id: str,
        op: str,
        completed: bool,
        title: Optional[str],
        year: Optional[int],
        month: Optional[int],
        day: Optional[int],
        hour: Optional[int],
        minute: Optional[int],
        add_error: Optional[str],
        search_error: Optional[str],
    ):
        self.line_id = line_id
        self.op = op
        self.completed = completed
        self.title = title
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.add_error = add_error
        self.search_error = search_error


class PlanList(db.Model):
    """F3 予定リスト

    Attributes:
        id: 予定リスト ID
        line_id: Line ID
        plan_id: 予定 ID
    """

    id: int = db.Column(db.Integer, primary_key=True)
    line_id: str = db.Column(db.String(50), nullable=False)
    plan_id: int = db.Column(db.Integer, nullable=False)

    def __init__(self, line_id: str, plan_id: int):
        self.line_id = line_id
        self.plan_id = plan_id


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
    return new_plan_detail(title, line_id, None, notif_time, start_time, None, None)


def new_plan_detail(
    title: str,
    line_id: str,
    detail: Optional[str],
    notif_time: StrictDateTime,
    allday: Optional[StrictDateTime],
    start_time: Optional[StrictDateTime],
    end_time: Optional[StrictDateTime],
) -> Plan:
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
    return Plan(
        title,
        line_id,
        detail,
        notif_time.into(),
        into_datatime(allday),
        into_datatime(start_time),
        into_datatime(end_time),
    )
