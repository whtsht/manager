from flask import Blueprint


web = Blueprint("web", __name__, url_prefix="/web")


# テスト関数
@web.route("/hello/", methods=["GET"])
def hello():
    return "hello :)"
