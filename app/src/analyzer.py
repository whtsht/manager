"""
Designer:   東間日向
Date:       2023/06/27
Purpose:    C2 意味解析のラッパー関数群
"""
import subprocess
import json
from info import InputInfo, Time, Date, DateTime, OP
from typing import Optional


def operation_from_str(op_str: Optional[str]) -> Optional[OP]:
    if op_str == "Search":
        return OP.Search
    if op_str == "Add":
        return OP.Add

    return None


def time_from_dict(obj: dict[str, Optional[int]]) -> Time:
    return Time(obj["hour"], obj["minute"])


def date_from_dict(obj: dict[str, Optional[int]]) -> Date:
    return Date(obj["year"], obj["month"], obj["day"])


def datetime_from_dict(obj: dict[str, dict[str, Optional[int]]]) -> DateTime:
    return DateTime(
        date_from_dict(obj["date"]),
        time_from_dict(obj["time"]),
    )


def input_info_from_dict(json) -> InputInfo:
    return InputInfo(
        json["title"],
        operation_from_str(json["operation"]),
        datetime_from_dict(json["date_time"]),
    )


def analyze_message(input: str) -> InputInfo:
    response = subprocess.check_output(["analyze", f'"{input}"'], encoding="utf-8")
    return input_info_from_dict(json.loads(response))
