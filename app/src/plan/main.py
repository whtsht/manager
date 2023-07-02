"""
Designer:   菊地智遥, 小田桐光佑, 東間日向
Date:       2023/06/27
Purpose:    対話処理の状態管理，制御関数群
"""
from info import InputInfo, Plan, UserState, OP, SearchError
from analyzer import analyze_message
from plan import add, search
from plan.notify import snooze


status: dict[str, UserState] = {}


def main(message: str, line_id: str) -> str:
    if message == "5分 スヌーズ":
        return snooze(line_id, 5)
    if message == "10分 スヌーズ":
        return snooze(line_id, 10)
    if message == "15分 スヌーズ":
        return snooze(line_id, 15)

    input_info = analyze_message(message)
    input_info = integrate_input(line_id, input_info)
    if input_info.op == OP.Add:
        result = add.from_message(line_id, input_info.into_plan_info())
        if result is None:
            status[line_id] = UserState(
                OP.Add, True, input_info.into_plan_info(), None, None, None
            )
        else:
            status[line_id] = UserState(
                OP.Add, False, input_info.into_plan_info(), None, result, None
            )
    elif input_info.op == OP.Search:
        result = search.from_message(line_id, input_info.into_plan_info())

        if type(result) is list:
            status[line_id] = UserState(
                OP.Search, True, input_info.into_plan_info(), result, None, None
            )
        else:
            status[line_id] = UserState(
                OP.Search, False, input_info.into_plan_info(), None, None, result  # type: ignore
            )
    else:
        return (
            "すみません，よくわかりませんでした．"
            + "予定の追加または検索のどちらかを指定してください．\n"
            + "例) 予定を追加したい場合\n"
            + "「明日はXXX」\n\n"
            + "例) 予定を検索したい場合\n"
            + "「明日の予定はある？」"
        )

    return gen_message(line_id)


def integrate_input(line_id: str, input_info: InputInfo) -> InputInfo:
    """利用者の現在の状態と入力を統合する
    Args: line_id:LineID
          input_info:入力情報
    Returns: Input_info:入力情報
    """
    if line_id in status:
        input_info.title = input_info.title or status[line_id].plan_info.title
        input_info.op = input_info.op or status[line_id].op
        input_info.start_time = (
            input_info.start_time or status[line_id].plan_info.start_time
        )
    return input_info


def gen_message(lineID: str) -> str:
    """M19 現在の利用者の状態から返答メッセージを生成する.
    .statusからop/complitedを取り出す.
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
