"""
Designer    : 東間日向
Date        : 2023/06/27
Purpose     : Line SDK との連携
"""
from flask import request, abort, Blueprint
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from plan.main import main
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)
from secret import (
    CHANNEL_ACCESS_TOKEN,
    CHANNEL_SECRET,
)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


line = Blueprint("line", __name__)


@line.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    response = main(event.message.text, event.source.user_id)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
