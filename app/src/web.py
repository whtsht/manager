"""
Designer:   東間日向
Date:       2023/06/27
Purpose:    C9 リクエスト処理に関するモジュール群
"""

from flask import request, jsonify
from db_models import Plan, db
from flask import Blueprint


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


@web.route("/add_plan/", methods=["POST"])
def add_plan():
    """M35 予定追加処理
    """
    if data := request.json:
        plan = data["plan"]
        db.session.add(plan)
        db.session.commit()

    return "ok"


@web.route("/modify_plan/", methods=["POST"])
def modify_plan():
    """M36 予定修正処理
    """
    if data := request.json:
        plan: Plan = data["plan"]
        db_plan: Plan = Plan.query.filter_by(Plan.id == plan.id).first()
        db_plan.title = plan.title
        db_plan.detail = plan.detail
        db_plan.notif_time = plan.notif_time
        db_plan.allday = plan.allday
        db_plan.start_time = plan.start_time
        db_plan.end_time = plan.end_time
        db.session.commit()

    return "ok"


@web.route("/remove_plan/", methods=["POST"])
def remove_plan():
    """M37 予定削除処理
    """
    if data := request.json:
        plan_id = data["planID"]
        Plan.query.filter_by(Plan.id == plan_id).delete()
        db.session.commit()
    return "ok"
