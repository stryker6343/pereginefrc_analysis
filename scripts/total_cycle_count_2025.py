from os import getenv

from pandasgui import show

from peregrinefrc_analysis import PeregrineClient
from peregrinefrc_analysis.analysis import make_team_dataframe
from peregrinefrc_analysis.analysis_2025 import COUNT_FUNCTIONS, COUNT_NAMES

EVENT_IDS = ["2025orsal", "2025waahs", "2025orore", "2025wabon", "2025wasam", "2025wasno", "2025wayak", "2025orwil"]

client = PeregrineClient()
client.authenticate(
    username=getenv("PEREGRINE_USERNAME"), password=getenv("PEREGRINE_PASSWORD")
)

df = make_team_dataframe(
    client, EVENT_IDS, COUNT_NAMES, COUNT_FUNCTIONS, excluded_reports=None
)
show(df)
