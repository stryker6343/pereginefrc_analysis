CORAL_SCORES = {"Coral L1 (auto)": 3,
                "Coral L2 (auto)": 4,
                "Coral L3 (auto)": 6,
                "Coral L4 (auto)": 7,
                "Coral L1 (teleop)": 2,
                "Coral L2 (teleop)": 3,
                "Coral L3 (teleop)": 4,
                "Coral L4 (teleop)": 5,
                }


def count_total_game_pieces(entry_data: dict) -> int:
    result = 1 if "Coral" in entry_data["name"] or "Algae" in entry_data["name"] else 0
    return result


def count_total_coral(entry_data: dict) -> int:
    result = 1 if "Coral" in entry_data["name"] else 0
    return result


def count_total_algae(entry_data: dict) -> int:
    result = 1 if  "Algae" in entry_data["name"] else 0
    return result


def count_coral_score(entry_data: dict) -> int:
    try:
        return CORAL_SCORES[entry_data["name"]]
    except KeyError:
        return 0


COUNT_FUNCTIONS = [
    count_total_game_pieces,
    count_total_coral,
    count_total_algae,
    count_coral_score,
]

COUNT_NAMES = [
    "Total Game Pieces",
    "Total Coral",
    "Total Algae",
    "Total Coral Score",
]
