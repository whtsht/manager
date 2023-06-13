from datetime import datetime

dependency: dict[str, set[str]] = {
    # Component 1
    "1": set({}),
    "2": set({}),
    "3": set({}),
    "4": set({}),
    "5": {"6", "13"},
    "6": {"7", "12"},
    "7": {"1"},
    "8": {"2"},
    "9": {"10", "11"},
    "10": {"3"},
    "11": {"4"},
    "12": set({}),
    "13": set({}),
    # Component 2
    "14": {"15", "16"},
    "15": set({}),
    "16": set({}),
    # Component 3
    "17": {"18", "19"},
    "18": set({}),
    "19": set({}),
    # Component 4
    "20": set({}),
    "21": {"20"},
    "22": set({}),
    "23": {"21"},
    "24": {"23"},
    # Component 5
    "25": {"26"},
    "26": set({}),
    "27": set({}),
    "28": set({}),
    # Component 6
    "29": set({}),
    # Component 7
    "30": set({}),
    # Component 8
    "31": set({}),
    "32": set({}),
    "33": set({}),
    # Component 9
    "34": set({}),
    "35": set({}),
    "36": set({}),
    "37": set({}),
}

code_par_day = {"東間日向": 70.0, "石川隼": 25.0, "菊地智遥": 25.0, "小田桐光佑": 25.0}

start_day = datetime(2023, 6, 13)
