from analyzer import analyze_message
from info import OP


def test_add_request(client):
    input_info = analyze_message("明日は学校")
    assert input_info.op == OP.Add
    assert input_info.title == "学校"
    assert input_info.start_time.date.year is not None
    assert input_info.start_time.date.month is not None
    assert input_info.start_time.date.day is not None
    assert input_info.start_time.time.hour is None
    assert input_info.start_time.time.minute is None

    input_info = analyze_message("2023/7/11の16:30からバイト")
    assert input_info.op == OP.Add
    assert input_info.title == "バイト"
    assert input_info.start_time.date.year == 2023
    assert input_info.start_time.date.month == 7
    assert input_info.start_time.date.day == 11
    assert input_info.start_time.time.hour == 16
    assert input_info.start_time.time.minute == 30


def test_search_request(client):
    input_info = analyze_message("明日の予定は？")
    assert input_info.op is OP.Search
