from os import getenv

from pandasgui import show

from peregrinefrc_analysis import PeregrineClient
from peregrinefrc_analysis.analysis import make_team_dataframe
from peregrinefrc_analysis.analysis_2025 import COUNT_FUNCTIONS, COUNT_NAMES
from peregrinefrc_analysis import BlueAllianceClient

EVENT_IDS = ["2025orsal", "2025wasno", "2025orore", "2025wasam", "2025wayak", "2025wabon", "2025waahs", "2025orwil"]
DISTRICT = "2025pnw"


def main():
    blue_alliance = BlueAllianceClient(getenv("X-TBA-Auth-Key"))
    rankings = blue_alliance.district_rankings(DISTRICT)
    peregrine = PeregrineClient()
    peregrine.authenticate(
        username=getenv("PEREGRINE_USERNAME"), password=getenv("PEREGRINE_PASSWORD")
    )

    df = make_team_dataframe(
        peregrine, EVENT_IDS, COUNT_NAMES, COUNT_FUNCTIONS, rankings, excluded_reports=None
    )
    show(df)

if __name__ == "__main__":
    main()
