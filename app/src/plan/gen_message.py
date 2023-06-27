"""
Dedigner: 小田桐光佑
Date: 2023/6/27
Purpose:M19 現在の利用者の状態から返答メッセージを生成する.
"""
from plan import add, search
from plan.main import status
from info import OP


def gen_message(lineID: str):
    """.statusからop/complitedを取り出す.
    もしAdd/TrueならばM28を呼び出す.
    もしAdd/FalseならばM27を呼び出す.
    もしSearch/TrueならばM33を呼び出す.
    もしSearch/FalseならばM32を呼び出す.

    Args:
        lineID (str): lineID
        PlanInfo (plan_info): 予定情報
        AddError (error): 予定情報エラー
        list (Plan): 予定リスト
        SerchError (error): 検索エラー
    """
    st = status[lineID]
    message = ""
    if st.op == OP.Add and st.completed is True:
        message = add.complited_message(st.plan_info)
        del status[lineID]

    elif st.op == OP.Add and st.completed is False:
        message = add.uncompleted_message(st.add_error)  # type: ignore

    elif st.op == OP.Search and st.completed is True:
        message = search.completed_message(st.plan_info, st.plan_list)  # type: ignore
        del status[lineID]

    elif st.op == OP.Search and st.completed is False:
        message = search.uncompleted_message(st.search_error)  # type: ignore

    return message
