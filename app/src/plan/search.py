"""
Designer:   石川隼
Date:       2023/06/26
Purpose:    予定検索
"""

from info import PlanInfo, Plan, SearchError, SearchErrorType, get_start_time


def from_message(_: str, plan_info: PlanInfo) -> list[Plan] | SearchErrorType:
    """M31 予定検索処理 データベースから予定を検索

    Args:
        line_id (str): LINEのid
        plan_info (PlanInfo): 予定情報

    Returns:
        Plan (list || SearchErrorType): エラーの詳細、予定の詳細
    """
    # タイトルも日付も指定されない．エラー
    if plan_info.title is None and plan_info.start_time.date.day is None:
        return SearchErrorType.LackInfo

    # タイトルのみ
    if plan_info.title is not None and plan_info.start_time.date.day is None:
        plans = Plan.query.filter(Plan).filter(Plan.title == plan_info.title).all()
        if len(plans) == 0:
            return SearchErrorType.NotFound
        else:
            return plans

    # 日付のみ
    if plan_info.title is None and plan_info.start_time.date.day is not None:
        plans = (
            Plan.query.filter(Plan)
            .filter(get_start_time(Plan).day == plan_info.start_time.date.day)
            .all()
        )
        if len(plans) == 0:
            return SearchErrorType.NotFound
        else:
            return plans

    # 両方指定されている
    plans = (
        Plan.query.filter(Plan)
        .filter(Plan.title == plan_info.title)
        .filter(get_start_time(Plan).day == plan_info.start_time.date.day)
        .all()
    )
    if len(plans) == 0:
        return SearchErrorType.NotFound
    else:
        return plans


def uncompleted_message(error: SearchError) -> str:
    """M32 検索情報不足通知 検索できなかった場合の応答

    Args:
        error (SearchError): 検索処理のエラータイプ

    Returns:
        (str): エラーメッセージ
    """
    if error.error_type == SearchErrorType.NotFound:
        return "予定を見つけることができませんでした。"

    return "予定のタイトル、日付のどちらかを入力して下さい。"


def completed_message(_: PlanInfo, plan_list: list[Plan]) -> str:
    """M33 予定送信処理 検索された予定の情報を知らせる

    Args:
        plan_info (PlanInfo): 予定情報
        plan_list (list[Plan]): 予定のリスト

    Returns:
        mes (str): メッセージ
    """
    mes = "予定が見つかりました。\n"

    for i in range(len(plan_list)):
        mes += plan_list[i].title + "\n"
        mes += str(plan_list[i].start_time or plan_list[i].allday) + "\n\n"
    return mes
