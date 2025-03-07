from os import getenv

from peregrinefrc_analysis import PeregrineClient
from peregrinefrc_analysis.analysis import make_team_dataframe
from peregrinefrc_analysis.analysis_2023 import COUNT_FUNCTIONS, COUNT_NAMES

EVENT_IDS = ["2023orwil"]
EXCLUDED_REPORTS = [9531, 9532]


def main():
    client = PeregrineClient()
    client.authenticate(
        username=getenv("PEREGRINE_USERNAME"), password=getenv("PEREGRINE_PASSWORD")
    )
    df = make_team_dataframe(
        client, EVENT_IDS, COUNT_NAMES, COUNT_FUNCTIONS, excluded_reports=EXCLUDED_REPORTS
    )
    print(df)

if __name__ == "__main__":
    main()
