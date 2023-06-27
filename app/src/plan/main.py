from info import InputInfo
from info import UserState

status: dict[str, UserState] = {}


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
