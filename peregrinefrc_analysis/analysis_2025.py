def count_total_game_pieces(entry_data: dict) -> bool:
    return "Coral" in entry_data["name"] or "Algae" in entry_data["name"]


def count_total_coral(entry_data: dict) -> bool:
    return "Coral" in entry_data["name"]


def count_total_algae(entry_data: dict) -> bool:
    return "Algae" in entry_data["name"]


COUNT_FUNCTIONS = [
    count_total_game_pieces,
    count_total_coral,
    count_total_algae,
]
COUNT_NAMES = [
    "Total Game Pieces",
    "Total Coral",
    "Total Algae",
]
