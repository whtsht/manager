from db_models import db, Plan
from info import PlanInfo, AddError


def from_message(lineID: str, plan_info: PlanInfo):
    pass


def add_plan(plan: Plan):
    db.session.add(plan)
    db.session.comit()


def uncompleted_message(error: AddError):
    if error.error_type == 1:
        return "その予定は既に追加されています"
    if error.error_type == 2:
        return "タイトルが設定されていません"
    if error.error_type == 3:
        return "開始時間が設定されていません"


def complited_message(plan_info: PlanInfo):
    return f"予定の追加が完了しました。タイトルは{plan_info.title}、開始時間は{plan_info.start_time}です。"
