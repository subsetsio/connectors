"""Opportunity Insights Economic Tracker downloads."""

from __future__ import annotations

import gzip
import os
import tempfile

import duckdb
from subsets_utils import NodeSpec, get, save_raw_parquet


BASE_URL = "https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data"

# entity_id -> GitHub data filename. The accepted catalog is the Economic Tracker
# only; static Opportunity Insights paper extracts are rejected at accept stage.
FILES = {
    "tracker-affinity-city-daily": "Affinity - City - Daily.csv",
    "tracker-affinity-city-monthly": "Affinity - City - Monthly.csv",
    "tracker-affinity-county-daily": "Affinity - County - Daily.csv",
    "tracker-affinity-county-monthly": "Affinity - County - Monthly.csv",
    "tracker-affinity-daily-total-spending-national": "Affinity Daily Total Spending - National.csv",
    "tracker-affinity-income-shares-national-2019": "Affinity Income Shares - National - 2019.csv",
    "tracker-affinity-income-shares-national-2020": "Affinity Income Shares - National - 2020.csv",
    "tracker-affinity-industry-composition-national-2020": "Affinity Industry Composition - National - 2020.csv",
    "tracker-affinity-national-daily": "Affinity - National - Daily.csv",
    "tracker-affinity-national-monthly": "Affinity - National - Monthly.csv",
    "tracker-affinity-state-daily": "Affinity - State - Daily.csv",
    "tracker-affinity-state-monthly": "Affinity - State - Monthly.csv",
    "tracker-covid-city-daily": "COVID - City - Daily.csv",
    "tracker-covid-county-daily-2020": "COVID - County - Daily 2020.csv",
    "tracker-covid-county-daily-2021": "COVID - County - Daily 2021.csv.gz",
    "tracker-covid-county-daily-2022": "COVID - County - Daily 2022.csv.gz",
    "tracker-covid-county-daily-2023": "COVID - County - Daily 2023.csv",
    "tracker-covid-national-daily": "COVID - National - Daily.csv",
    "tracker-covid-state-daily": "COVID - State - Daily.csv",
    "tracker-earnin-zcta-2020": "Earnin - ZCTA - 2020.csv",
    "tracker-employment-city-weekly": "Employment - City - Weekly.csv",
    "tracker-employment-county-weekly": "Employment - County - Weekly.csv",
    "tracker-employment-national-weekly": "Employment - National - Weekly.csv",
    "tracker-employment-state-weekly": "Employment - State - Weekly.csv",
    "tracker-geoids-city": "GeoIDs - City.csv",
    "tracker-geoids-county": "GeoIDs - County.csv",
    "tracker-geoids-state": "GeoIDs - State.csv",
    "tracker-google-mobility-city-daily": "Google Mobility - City - Daily.csv",
    "tracker-google-mobility-county-daily": "Google Mobility - County - Daily.csv.gz",
    "tracker-google-mobility-national-daily": "Google Mobility - National - Daily.csv",
    "tracker-google-mobility-state-daily": "Google Mobility - State - Daily.csv",
    "tracker-job-postings-city-weekly": "Job Postings - City - Weekly.csv",
    "tracker-job-postings-county-weekly": "Job Postings - County - Weekly.csv",
    "tracker-job-postings-industry-shares-national-2020": "Job Postings Industry Shares - National - 2020.csv",
    "tracker-job-postings-national-weekly": "Job Postings - National - Weekly.csv",
    "tracker-job-postings-state-weekly": "Job Postings - State - Weekly.csv",
    "tracker-policy-milestones-state": "Policy Milestones - State.csv",
    "tracker-ui-claims-city-weekly": "UI Claims - City - Weekly.csv",
    "tracker-ui-claims-county-weekly": "UI Claims - County - Weekly.csv",
    "tracker-ui-claims-national-weekly": "UI Claims - National - Weekly.csv",
    "tracker-ui-claims-state-weekly": "UI Claims - State - Weekly.csv",
    "tracker-womply-city-weekly": "Womply - City - Weekly.csv",
    "tracker-womply-county-weekly": "Womply - County - Weekly.csv",
    "tracker-womply-national-weekly": "Womply - National - Weekly.csv",
    "tracker-womply-state-weekly": "Womply - State - Weekly.csv",
    "tracker-womply-zcta-2020": "Womply - ZCTA - 2020.csv",
    "tracker-zearn-city-weekly": "Zearn - City - Weekly.csv",
    "tracker-zearn-county-weekly": "Zearn - County - Weekly.csv",
    "tracker-zearn-national-weekly": "Zearn - National - Weekly.csv",
    "tracker-zearn-state-weekly": "Zearn - State - Weekly.csv",
}


def _raw_url(filename: str) -> str:
    from urllib.parse import quote

    return f"{BASE_URL}/{quote(filename)}"


def _csv_to_table(raw: bytes):
    fd, path = tempfile.mkstemp(suffix=".csv")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(raw)
        con = duckdb.connect()
        try:
            return con.sql(
                f"SELECT * FROM read_csv_auto('{path}', sample_size=-1)"
            ).to_arrow_table()
        finally:
            con.close()
    finally:
        os.unlink(path)


def fetch_one(node_id: str) -> None:
    entity_id = node_id.removeprefix("opportunity-insights-")
    filename = FILES[entity_id]
    resp = get(_raw_url(filename), timeout=(10.0, 300.0))
    resp.raise_for_status()
    raw = resp.content
    if filename.endswith(".gz"):
        raw = gzip.decompress(raw)
    table = _csv_to_table(raw)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"opportunity-insights-{entity_id}", fn=fetch_one)
    for entity_id in FILES
]
