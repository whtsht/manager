"""
Designer:   東間日向
Date:       2023/06/17
Purpose:    他モジュールで使うクラスの定義
"""
from typing import Optional
from datetime import datetime
from db_models import Plan
from enum import Enum


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
        return datetime(
            self.year,
            self.month,
            self.day,
            self.hour,
            0 if self.minute == None else self.minute,
        )


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


class UserState:
    """利用者の入力情報を表す
    Attributes:
        op (OP):
            操作
        completed (bool):
            処理が完了したかどうか
        plan_info (PlanInfo):
            予定情報
        plan_list (Optional[list[Plan]]):
            検索した予定のリスト．追加操作では使わない
    """

    def __init__(
        self,
        op: OP,
        completed: bool,
        plan_info: PlanInfo,
        plan_list: Optional[list[Plan]],
    ):
        self.op = op
        self.completed = completed
        self.plan_info = plan_info
        self.plan_list = plan_list


class AddErrorType(Enum):
    """追加処理エラータイプ"""

    AlreadyExist = 1
    TitleNotSet = 2
    TimeNotSet = 3


class AddError:
    """追加処理エラー情報

    attributes:
        error_type (AddErrorType):
            エラータイプ
        title      (Optional[str]):
            タイトル
        start_time (Optional[DateTime]):
            開始時刻
    """

    def __init__(
        self,
        error_type: AddErrorType,
        title: Optional[str] = None,
        start_time: Optional[DateTime] = None,
    ):
        self.error_type = error_type
        self.title = title
        self.start_time = start_time


class SearchErrorType(Enum):
    """検索処理のエラータイプ"""
    NotFound = 1
    LackInfo = 2

class SearchError:
    """追加処理エラー情報

    attributes:
        error_type (SearchErrorType):
            エラータイプ
        title      (Optional[str]):
            タイトル
    """
    
    def __init__(self, error_type: SearchErrorType, title: Optional[str] = None):
        self.error_type = error_type
        self.title = title
