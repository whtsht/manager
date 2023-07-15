"""
Designer:   菊地智遥, 小田桐光佑, 東間日向
Date:       2023/06/27
Purpose:    対話処理の状態管理，制御関数群
"""
from info import (
    InputInfo,
    Plan,
    PlanInfo,
    UserState,
    OP,
    SearchError,
    db,
    AddError,
    PlanList,
    DateTime,
    Date,
    Time,
)
from analyzer import analyze_message
from plan import add, search
from plan.notify import snooze


def main(message: str, line_id: str) -> str:
    if message == "説明 追加":
        return """追加する予定の開始時刻，予定名を教えてください\n
例) 明日の16:00にレポートという予定を追加する場合\n
追加 明日 16:00 レポート\n\n
例) 今年の11/12の9:00に試験という予定を追加する場合\n
追加 11/12 9:00 レポート"""
    if message == "説明 検索":
        return """検索する時間またはタイトルを教えてください\n
例) 明日の予定を検索したい場合\n
検索 明日\n\n
例) レポートという名前の予定を検索したい場合\n
検索 レポート"""

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
            state = UserState(
                line_id,
                "Add",
                True,
                input_info.title,
                input_info.start_time.date.year,
                input_info.start_time.date.month,
                input_info.start_time.date.day,
                input_info.start_time.time.hour,
                input_info.start_time.time.minute,
                None,
                None,
            )
            update_user_state(state)
        else:
            error = ""
            if result == AddError.AlreadyExist:
                error = "AlreadyExist"
            elif result == AddError.TimeNotSet:
                error = "TimeNotSet"
            elif result == AddError.DateNotSet:
                error = "DateNotSet"
            elif result == AddError.DateTimeNotSet:
                error = "DateTimeNotSet"
            else:
                error = "TitleNotSet"
            state = UserState(
                line_id,
                "Add",
                False,
                input_info.title,
                input_info.start_time.date.year,
                input_info.start_time.date.month,
                input_info.start_time.date.day,
                input_info.start_time.time.hour,
                input_info.start_time.time.minute,
                error,
                None,
            )
            update_user_state(state)
    elif input_info.op == OP.Search:
        result = search.from_message(line_id, input_info.into_plan_info())

        if type(result) is list:
            state = UserState(
                line_id,
                "Search",
                True,
                input_info.title,
                input_info.start_time.date.year,
                input_info.start_time.date.month,
                input_info.start_time.date.day,
                input_info.start_time.time.hour,
                input_info.start_time.time.minute,
                None,
                None,
            )
            update_user_state(state)

            for plan in result:
                plan_list = PlanList(line_id, plan.id)
                db.session.add(plan_list)
                db.session.commit()
        else:
            error = ""
            if result == SearchError.NotFound:
                error = "NotFound"
            else:
                error = "LackInfo"
            state = UserState(
                line_id,
                "Search",
                False,
                input_info.title,
                input_info.start_time.date.year,
                input_info.start_time.date.month,
                input_info.start_time.date.day,
                input_info.start_time.time.hour,
                input_info.start_time.time.minute,
                None,
                error,
            )
            update_user_state(state)

    else:
        return (
            "すみません，よくわかりませんでした．\n"
            + "予定の追加または検索のどちらかを指定してください．\n"
            + "例) 予定を追加したい場合\n"
            + "「明日はXXX」\n\n"
            + "例) 予定を検索したい場合\n"
            + "「明日の予定はある？」"
        )

    return gen_message(line_id)


def update_user_state(state: UserState):
    old_state: UserState = UserState.query.filter(
        UserState.line_id == state.line_id
    ).first()
    if old_state is None:
        db.session.add(state)
    else:
        old_state.op = state.op
        old_state.completed = state.completed
        old_state.title = state.title
        old_state.year = state.year
        old_state.month = state.month
        old_state.day = state.day
        old_state.hour = state.hour
        old_state.add_error = state.add_error
        old_state.search_error = state.search_error

    db.session.commit()


def integrate_input(line_id: str, input_info: InputInfo) -> InputInfo:
    """利用者の現在の状態と入力を統合する
    Args: line_id:LineID
          input_info:入力情報
    Returns: Input_info:入力情報
    """
    state: UserState = UserState.query.filter(UserState.line_id == line_id).first()
    if state is not None:
        input_info.title = input_info.title or state.title
        if state.op == "Add":
            input_info.op = input_info.op or OP.Add
        elif state.op == "Search":
            input_info.op = input_info.op or OP.Search
        input_info.start_time = DateTime(
            Date(
                input_info.start_time.date.year or state.year,
                input_info.start_time.date.month or state.month,
                input_info.start_time.date.day or state.day,
            ),
            Time(
                input_info.start_time.time.hour or state.hour,
                input_info.start_time.time.minute,
            ),
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
    st: UserState = UserState.query.filter(UserState.line_id == lineID).first()
    message = ""
    if st.op == "Add" and st.completed is True:
        plan_info = PlanInfo(
            st.title,
            DateTime(Date(st.year, st.month, st.day), Time(st.hour, st.minute)),
        )
        message = add.complited_message(plan_info)

    elif st.op == "Add" and st.completed is False:
        if st.add_error == "AlreadyExist":
            message = add.uncompleted_message(AddError.AlreadyExist)
        elif st.add_error == "TimeNotSet":
            message = add.uncompleted_message(AddError.TimeNotSet)
        elif st.add_error == "DateNotSet":
            message = add.uncompleted_message(AddError.DateNotSet)
        elif st.add_error == "DateTimeNotSet":
            message = add.uncompleted_message(AddError.DateTimeNotSet)
        else:
            message = add.uncompleted_message(AddError.TitleNotSet)

    elif st.op == "Search" and st.completed is True:
        plan_id_list = PlanList.query.filter(PlanList.line_id == lineID).all()
        plan_id_list = list(map(lambda planlist: planlist.plan_id, plan_id_list))
        plan_list = list(
            map(lambda id: Plan.query.filter(Plan.id == id).first(), plan_id_list)
        )
        message = search.completed_message(plan_list)

    elif st.op == "Search" and st.completed is False:
        if st.search_error == "NotFound":
            message = search.uncompleted_message(SearchError.NotFound)
        else:
            message = search.uncompleted_message(SearchError.LackInfo)

    db.session.delete(st)
    PlanList.query.filter(PlanList.line_id == lineID).delete()
    db.session.commit()

    return message
