from io import TextIOWrapper
import math
from copy import copy
import re
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import csv
import config

def get_tasks(report: list[list[str]]) -> defaultdict[str, list[dict[str, str]]]:
    ret = defaultdict(lambda: [])
    for r in report:
        value = {}
        if component := re.search(r"\d+", r[0]):
            value["component"] = str(component.group(0))
            value["comopoent_name"] = r[0]
        if module := re.search(r"\d+", r[1]):
            value["module"] = str(module.group(0))
            value["module_name"] = r[1]
        value["code"] = r[3]
        value["ps"] = r[4]

        ret[r[2]].append(value)
    return ret


def skip_lines(file: TextIOWrapper, line: int):
    for _ in range(line):
        file.readline()


def get_depend(graph: dict[str, set[str]]) -> dict[str, int]:
    indegree = {}
    for key, value in graph.items():
        indegree[key] = len(value)
    return indegree


def topological_sort(graph: dict[str, set[str]], indegree: dict[str, int]):
    sorted_list: list[str] = []
    stack = []

    keys = sorted(list(graph.keys()), reverse=True)
    for key in keys:
        if indegree[key] == 0:
            stack.append(key)

    # while not queue.empty():
    while len(stack) != 0:
        v = stack.pop()

        for u in graph[v]:
            indegree[u] -= 1
            if indegree[u] == 0:
                stack.append(u)

        sorted_list.append(v)

    return sorted_list


if __name__ == "__main__":
    tasks_dict = {}

    with open("./report.csv", "r") as report:
        skip_lines(report, 10)
        report = csv.reader(report)
        tasks_dict = get_tasks(list(report))

    assign_dict = {
        name: list(map(lambda v: str(v["module"]), tasks))
        for name, tasks in tasks_dict.items()
    }

    depend = get_depend(config.dependency)

    active_tasks = []
    for key, value in depend.items():
        if value == 0:
            active_tasks.append(key)

    d = defaultdict(lambda: set({}))
    for key, value in config.dependency.items():
        for v in value:
            d[v].add(key)

    assignees = {"東間日向": 0, "石川隼": 0, "菊地智遥": 0, "小田桐光佑": 0}

    sorted_tasks_dict: dict[str, list[tuple[int, int, str, str]]] = defaultdict(list)

    def not_assigned(d: dict[str, int]):
        return len(list(filter(lambda v: v == 0, d.values()))) != 0

    day = 0
    while len(active_tasks) != 0:
        current_tasks: list[str] = copy(active_tasks)

        while not_assigned(assignees) and len(current_tasks) != 0:
            v = current_tasks.pop(0)

            for name, tasks in assign_dict.items():
                if v in tasks and assignees[name] == 0:
                    value = next(
                        filter(lambda task: task["module"] == v, tasks_dict[name])
                    )
                    code = float(value["code"])
                    module_name = str(value["module_name"])
                    state = str(value["ps"])
                    time = int(math.ceil(code / config.code_par_day[name]))
                    assignees[name] = time
                    sorted_tasks_dict[name].append((day, time, module_name, state))
                    for u in d[v]:
                        depend[u] -= 1
                        if depend[u] == 0:
                            active_tasks.append(u)
                    active_tasks.remove(v)

        day += 1
        for name in assignees.keys():
            if assignees[name] > 0:
                assignees[name] -= 1
    with open("./gantt.md", "w") as gantt, open("./limit.md", "w") as limit:
        gantt.write("```mermaid\n")
        gantt.write("gantt\n")
        gantt.write("dateFormat YYYY-MM-DD\n")

        limit.write("| 担当者 | モジュール名 | 期限 | 進捗 | 状態 |\n")
        limit.write("|--------|----------------|------|------|------|\n")

        for name, tasks in sorted_tasks_dict.items():
            gantt.write(f"section {name}\n")
            for dayoff, time, module_name, state in tasks:
                day = config.start_day + timedelta(days=dayoff)
                day_str = f"{day.year}-{day.month}-{day.day}"
                if state == "単体テスト完了":
                    gantt.write(f"{module_name} :done, {day_str}, {time}d\n")
                    limit.write(
                        f"| {name} | {module_name} | {(day + timedelta(days=time))} | {state} | 終了済み |\n"
                    )
                elif datetime.now() > (day + timedelta(days=time)):
                    gantt.write(f"{module_name} :crit, {day_str}, {time}d\n")
                    limit.write(
                        f"| {name} | {module_name} | {(day + timedelta(days=time))} | {state} | 遅れ |\n"
                    )
                else:
                    gantt.write(f"{module_name} :a1, {day_str}, {time}d\n")
                    limit.write(
                        f"| {name} | {module_name} | {(day + timedelta(days=time))} | {state} | 予定通り |\n"
                    )

        gantt.write("\n```")
