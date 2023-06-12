from flask import Blueprint

web = Blueprint("web", __name__, url_prefix="/web")


# テスト関数
@web.route("/hello/", methods=["GET"])
def hello():
    return "hello :)"


# TODO
# 予定のリストを返す
@web.route("/get_plan_list/", methods=["POST"])
def get_plan_list():
    return ""


# TODO
# 予定を追加する
@web.route("/add_plan/", methods=["POST"])
def add_plan():
    return ""


# TODO
# 予定を修正する
@web.route("/modify_plan/", methods=["POST"])
def modify_plan():
    return ""


# TODO
# 予定を削除する
@web.route("/remove_plan/", methods=["POST"])
def remove_plan():
    return ""
