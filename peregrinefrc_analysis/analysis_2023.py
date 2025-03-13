def count_total_game_pieces(entry_data: dict) -> int:
    return 1 if "Cubes" in entry_data["name"] or "Cones" in entry_data["name"] else 0


def count_total_cubes(entry_data: dict) -> int:
    return 1 if "Cubes" in entry_data["name"] else 0


def count_total_cones(entry_data: dict) -> int:
    return 1 if "Cones" in entry_data["name"] else 0


COUNT_FUNCTIONS = [
    count_total_game_pieces,
    count_total_cubes,
    count_total_cones,
]
COUNT_NAMES = [
    "Total Game Pieces",
    "Total Cubes",
    "Total Cones",
]
