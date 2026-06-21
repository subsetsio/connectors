"""UAD Aggregate Statistics — landing-page scrape for the versioned
county-level single-family zip, then unzip the CSV. County level (vs the
national file) keeps geoname/statefips/fips as rich dimensions instead of
constants, while staying bounded (~6M rows; the full/tract files are >5GB).

The UAD aggregate URL embeds a release-month folder + version suffix that both
move each release, so its link is scraped from the UAD landing page at fetch
time.
"""

from __future__ import annotations

import re

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import _csv_bytes_to_string_table, _get, _unzip_single_csv

UAD_LANDING = "https://www.fhfa.gov/data/uad"
UAD_LINK_RE = re.compile(r'href="(/sites/default/files/[^"]*UADAggs_ent_sf_county_v[^"]*\.zip)"')
UAD_COLS = [
    "SOURCE", "APPRAISALSOURCE", "SERIES", "SERIESID", "FREQUENCY", "GEOLEVEL",
    "GEONAME", "STATEPOSTAL", "STATEFIPS", "FIPS", "TRACT", "METRO", "PURPOSE",
    "YEAR", "QUARTER", "CHARACTERISTIC1", "CATEGORY1", "SUPPRESSED", "VALUE",
]


def fetch_uad_aggregate_statistics(node_id: str) -> None:
    page = _get(UAD_LANDING).text
    matches = UAD_LINK_RE.findall(page)
    if not matches:
        raise AssertionError(
            "could not locate UADAggs_ent_sf_county zip link on the UAD landing page"
        )
    href = matches[0]
    url = href if href.startswith("http") else f"https://www.fhfa.gov{href}"
    resp = _get(url)
    csv_bytes = _unzip_single_csv(resp.content)
    table = _csv_bytes_to_string_table(csv_bytes, UAD_COLS)
    table = table.rename_columns([c.lower() for c in table.column_names])
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fhfa-uad-aggregate-statistics", fn=fetch_uad_aggregate_statistics, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fhfa-uad-aggregate-statistics-transform",
        deps=["fhfa-uad-aggregate-statistics"],
        sql='''
            SELECT
                source, appraisalsource, series, seriesid, frequency, geolevel,
                geoname, statepostal, statefips, fips, purpose,
                CAST(NULLIF(year, '') AS INTEGER)    AS year,
                CAST(NULLIF(quarter, '') AS INTEGER) AS quarter,
                characteristic1, category1, suppressed,
                CAST(NULLIF(value, '') AS DOUBLE)    AS value
            FROM "fhfa-uad-aggregate-statistics"
        ''',
    ),
]
