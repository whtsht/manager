"""
Designer:   菊地智遥, 東間日向
Date:       2023/06/27
Purpose:    対話処理の状態管理，制御関数群
"""
from info import InputInfo, Plan, UserState, OP, SearchError
from analyzer import analyze_message
from plan import add, search, gen_message

status: dict[str, UserState] = {}


def main(message: str, line_id: str) -> str:
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
        if type(result) is list[Plan]:
            status[line_id] = UserState(
                OP.Search, True, input_info.into_plan_info(), result, None, None
            )
        elif type(result) is SearchError:
            status[line_id] = UserState(
                OP.Search, False, input_info.into_plan_info(), None, None, result
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

    return gen_message.gen_message(line_id)


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
