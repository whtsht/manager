"""
Designer:   東間日向
Date:       2023/06/27
Purpose:    C9 リクエスト処理に関するモジュール群
"""

from flask import request, jsonify
from info import Plan, db
from flask import Blueprint
from datetime import datetime
from plan import modify


web = Blueprint("web", __name__, url_prefix="/web")


# テスト関数
@web.route("/hello/", methods=["GET"])
def hello():
    return "hello :)"


@web.route("/get_plan_list/", methods=["POST"])
def get_plan_list():
    """M34 予定リスト取得処理

    Returns:
        Plan[]: 予定情報のリスト
    """
    if data := request.json:
        line_id = data["lineID"]
        plan_list = Plan.query.filter_by(Plan.line_id == line_id).all()
        return jsonify(plan_list)
    else:
        return jsonify([])


def to_datetime(value) -> datetime | None:
    return datetime.strptime(value, "%Y/%m/%dT%H:%M") if value is not None else None


def from_json(data: dict[str, any]) -> Plan:  # type: ignore
    title = data["title"]
    detail = data["detail"]
    line_id = data["lineID"]
    notif_time = datetime.strptime(data["notifTime"], "%Y/%m/%dT%H:%M")
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


@web.route("/add_plan/", methods=["POST"])
def add_plan():
    """M35 予定追加処理"""
    if data := request.json:
        new_plan = from_json(data["plan"])
        db.session.add(new_plan)
        db.session.commit()

    return "ok"


@web.route("/modify_plan/", methods=["POST"])
def modify_plan():
    """M36 予定修正処理"""
    if data := request.json:
        plan = from_json(data["plan"])
        modify.modify_plan(plan)
    return "ok"


@web.route("/remove_plan/", methods=["POST"])
def remove_plan():
    """M37 予定削除処理"""
    if data := request.json:
        plan_id = data["planID"]
        Plan.query.filter_by(Plan.id == plan_id).delete()
        db.session.commit()
    return "ok"
