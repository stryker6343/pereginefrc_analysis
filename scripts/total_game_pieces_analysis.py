from os import getenv

from peregrinefrc_analysis import PeregrineClient
from peregrinefrc_analysis.analysis_2023 import make_team_dataframe

EVENT_ID = "2023orwil"
EXCLUDED_REPORTS = [9531, 9532]

client = PeregrineClient()
client.authenticate(
    username=getenv("PEREGRINE_USERNAME"), password=getenv("PEREGRINE_PASSWORD")
)
df = make_team_dataframe(client, EVENT_ID, excluded_reports=EXCLUDED_REPORTS)
print(df)
