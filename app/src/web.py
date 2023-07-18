"""
Designer:   東間日向
Date:       2023/06/27
Purpose:    C9 リクエスト処理に関するモジュール群
"""

from flask import request
from info import Plan
from flask import Blueprint
from datetime import datetime
import json
from plan import modify, remove, add


web = Blueprint("web", __name__, url_prefix="/web")


# テスト関数
@web.route("/hello/", methods=["GET"])
def hello():
    return "hello :)"


@web.route("/get_plan_list/", methods=["POST"])
def get_plan_list():
    """M34 予定リスト取得処理
    M1からの要求を受け，予定のリストを返す．データベースから予定を取得しlineIDでフィルタリングし，残った予定リストを戻り値とする．予定が見つからなかったら空のリストを返す．
    """
    if data := request.json:
        line_id = data["lineID"]
        plan_list = Plan.query.filter(Plan.line_id == line_id).all()
        return plan_list_stringify(plan_list)
    else:
        return plan_list_stringify([])


def to_datetime(value) -> datetime | None:
    return datetime.strptime(value, "%Y/%m/%dT%H:%M") if value is not None else None


def time_stringify(value: datetime | None) -> str | None:
    if value:
        return value.strftime("%Y/%m/%dT%H:%M")
    else:
        return None


def from_json(data: dict[str, any]) -> Plan:  # type: ignore
    title = data["title"]
    detail = data["detail"]
    line_id = data["lineID"]
    notif_time = datetime.strptime(data["notifTime"], "%Y/%m/%dT%H:%M")
    print(data["allDay"])
    print(data["start"])
    allday = to_datetime(data["allDay"])
    start_time = to_datetime(data["start"])
    end_time = to_datetime(data["end"])
    return Plan(
        title,
        line_id,
        detail,
        notif_time,
        allday,
        start_time,
        end_time,
        data["id"] if "id" in data else None,
    )


def plan_list_stringify(plans: list[Plan]) -> str:
    plans_json = map(
        lambda plan: {
            "id": plan.id,
            "title": plan.title,
            "lineID": plan.line_id,
            "detail": plan.detail,
            "notifTime": time_stringify(plan.notif_time),
            "allDay": time_stringify(plan.allday),
            "start": time_stringify(plan.start_time),
            "end": time_stringify(plan.end_time),
        },
        plans,
    )
    return json.dumps(list(plans_json))


@web.route("/add_plan/", methods=["POST"])
def add_plan():
    """M35 予定追加処理
    M2からの要求を受け，予定を追加する．データベースにplanを追加する．主キーの予定IDは自動的にインクリメントされる．M21を呼び出し，通知の設定も行う．
    """
    if data := request.json:
        new_plan = from_json(data["plan"])
        add.add_plan(new_plan)

    return "ok"


@web.route("/modify_plan/", methods=["POST"])
def modify_plan():
    """M36 予定修正処理
    M3の要求を受け，予定を修正する．データベースからPlanのidと一致する予定を見つけ，それを更新する．
    """
    if data := request.json:
        plan = from_json(data["plan"])
        modify.modify_plan(plan)
    return "ok"


@web.route("/remove_plan/", methods=["POST"])
def remove_plan():
    """M37 予定削除処理
    M4の要求を受け，予定を削除する．データベースからplanIDの予定IDを持つ予定を削除する．M22を呼び出し，通知の削除も行う．
    """
    if data := request.json:
        plan_id = data["planID"]
        remove.remove_plan(plan_id)
    return "ok"
