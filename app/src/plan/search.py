"""
Designer:   石川隼
Date:       2023/06/26
Purpose:    予定検索
"""

from web import web
from info import PlanInfo, Plan, SearchError, SearchErrorType, db, get_start_time

def from_message(line_id:str, plan_info:PlanInfo):
    """M31 予定検索処理　データベースから予定を検索

    Args:
        line_id (str): LINEのid
        plan_info (PlanInfo): 予定情報

    Returns:
        Plan (list || SearchErrorType): エラーの詳細、予定の詳細
    """
    if plan_info.title is None and plan_info.start_time is None:
        return SearchErrorType.LackInfo

    elif db.session.query(Plan).filter(Plan.title == plan_info.title).filter(get_start_time(Plan) == plan_info.start_time).first() is None:
        return SearchErrorType.NotFound
    
    elif plan_info.title is None:
        #時間のみ
        return db.session.query(Plan).filter(get_start_time(Plan) == plan_info.start_time).all()
    
    else:
        #両方指定されている場合
        return db.session.query(Plan).filter(Plan.title == plan_info.title).filter(get_start_time(Plan) == plan_info.start_time).all()
    
def uncompleted_message(error: SearchError):
    """M32 検索情報不足通知　検索できなかった場合の応答

    Args:
        error (SearchError): 検索処理のエラータイプ

    Returns:
        (str): エラーメッセージ
    """
    if error.error_type == SearchErrorType.NotFound:
        return "予定を見つけることができませんでした。"
    if error.error_type == SearchErrorType.LackInfo:
        return "予定のタイトル、開始時刻のどちらかを入力して下さい。"
    

def completed_message(plan_info:PlanInfo, plan_list:list[Plan]):
    """M33 予定送信処理 検索された予定の情報を知らせる

    Args:
        plan_info (PlanInfo): 予定情報
        plan_list (list[Plan]): 予定のリスト

    Returns:
        mes (str): メッセージ 
    """
    mes = f"予定が見つかりました。タイトルは{plan_info.title}、開始時間は{plan_info.start_time}です。"
    return mes
