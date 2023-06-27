"""
Designer    : 東間日向
Date        : 2023/06/27
Purpose     : Line SDK との連携
"""
from flask import request, abort, Blueprint
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    ButtonsTemplate,
    TextSendMessage,
    MessageAction,
    TemplateSendMessage,
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
    response = event.message.text
    id = event.source.user_id
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
    push_buttons_message(id, "XXXの時間です", "スヌーズしたい場合は時間を選んでください", ["5分", "10分", "15分"])


def push_text_message(line_id: str, message: str):
    """利用者のLineにメッセージを送信する

    Args:
        line_id (str): Line ID
        message (str): メッセージ
    """
    line_bot_api.push_message(line_id, TextSendMessage(message))


def push_buttons_message(line_id: str, title: str, message: str, buttons: list[str]):
    """利用者にメッセージとボタンを送信する

    Args:
        line_id (str): Line ID
        title (str): タイトル
        message (str): メッセージ
        buttons (list[str]): ボタンに表示するメッセージ
    """
    buttons_template_message = TemplateSendMessage(
        alt_text="Buttons template",
        template=ButtonsTemplate(
            title=" " if len(title) == 0 else title,
            text=" " if len(message) == 0 else message,
            actions=map(
                lambda button: MessageAction(label=button, text=button), buttons
            ),
        ),
    )
    line_bot_api.push_message(line_id, buttons_template_message)
