"""Annual attendance subset.

park-attendance-attendance : historical ANNUAL attendance per park, scraped
from the per-park HTML tables at queue-times.com/parks/{id}/attendances. One
row per (park, year). Parks with no recorded data return HTTP 404 or an empty
table and are skipped. Stateless — re-pulled in full every run.

HTML parsing happens here in the fetch fn (structural surgery a SQL transform
can't do); the raw asset lands as clean parquet and the transform is a thin
cast/projection pass.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _get, _load_parks

ATTENDANCE_URL = "https://queue-times.com/parks/{park_id}/attendances"

ATTENDANCE_SCHEMA = pa.schema([
    ("park_id", pa.int64()),
    ("park_name", pa.string()),
    ("year", pa.int64()),
    ("annual_attendance", pa.int64()),
])


def _parse_attendance_table(html: str):
    """Return the Year/Attendance dataframe from a park attendance page, or an
    empty dataframe when the page has no usable table."""
    import pandas as pd
    from io import StringIO

    try:
        tables = pd.read_html(StringIO(html))
    except ValueError:
        return pd.DataFrame(columns=["Year", "Attendance"])
    for df in tables:
        if {"Year", "Attendance"}.issubset(set(df.columns)):
            return df
    return pd.DataFrame(columns=["Year", "Attendance"])


def fetch_attendance(node_id: str) -> None:
    """Scrape annual attendance for every park that publishes a table."""
    import pandas as pd

    asset = node_id
    parks = _load_parks()

    rows = []
    for park in parks:
        park_id = int(park["id"])
        park_name = park.get("name")
        resp = _get(ATTENDANCE_URL.format(park_id=park_id))
        if resp.status_code == 404:
            continue

        df = _parse_attendance_table(resp.text)
        if df.empty:
            continue

        # Attendance cells look like "17,250,000 [1]" — drop the footnote
        # marker and the thousands separators, then coerce to integer.
        att = (
            df["Attendance"].astype(str)
            .str.split(" ").str[0]
            .str.replace(",", "", regex=False)
        )
        att = pd.to_numeric(att, errors="coerce")
        year = pd.to_numeric(df["Year"], errors="coerce")

        for yr, count in zip(year, att):
            if pd.isna(yr) or pd.isna(count) or count <= 0:
                continue
            rows.append({
                "park_id": park_id,
                "park_name": park_name,
                "year": int(yr),
                "annual_attendance": int(count),
            })

    if not rows:
        raise ValueError("No attendance records scraped across any park")

    table = pa.Table.from_pylist(rows, schema=ATTENDANCE_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="park-attendance-attendance", fn=fetch_attendance, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="park-attendance-attendance-transform",
        deps=["park-attendance-attendance"],
        sql='''
            SELECT DISTINCT
                CAST(park_id AS BIGINT)           AS park_id,
                park_name,
                CAST(year AS BIGINT)              AS year,
                CAST(annual_attendance AS BIGINT) AS annual_attendance
            FROM "park-attendance-attendance"
            -- Floor out implausibly tiny values: a commercial theme park's
            -- annual attendance below 1,000 is not credible and indicates an
            -- upstream typo (e.g. queue-times lists Chimelong Ocean Kingdom
            -- 2013 as "11"). The lowest legitimate value observed is ~125,000.
            WHERE annual_attendance >= 1000
              AND year BETWEEN 1950 AND 2100
        ''',
    ),
]
