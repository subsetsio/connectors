"""STATS19 road safety open-data downloads.

DfT publishes three record-level STATS19 CSVs for the complete validated
history: collisions, vehicles, and casualties. The download normalizes them to
Parquet with a full-file DuckDB scan so late mixed-type coded columns are not
mis-inferred by transform-time CSV sampling.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

import duckdb

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get_client,
    raw_asset_exists,
    raw_writer,
)

SLUG = "stats19"
BASE_URL = "https://data.dft.gov.uk/road-accidents-safety-data"
CHUNK_SIZE = 1 << 20

URLS = {
    "stats19-collisions": (
        f"{BASE_URL}/dft-road-casualty-statistics-collision-1979-latest-published-year.csv"
    ),
    "stats19-vehicles": (
        f"{BASE_URL}/dft-road-casualty-statistics-vehicle-1979-latest-published-year.csv"
    ),
    "stats19-casualties": (
        f"{BASE_URL}/dft-road-casualty-statistics-casualty-1979-latest-published-year.csv"
    ),
}


def fetch_csv(node_id: str) -> None:
    url = URLS[node_id]
    client = get_client()
    with TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / f"{node_id}.csv"
        parquet_path = Path(tmpdir) / f"{node_id}.parquet"

        with client.stream("GET", url, timeout=(10.0, 1800.0)) as resp:
            resp.raise_for_status()
            content_type = resp.headers.get("content-type", "")
            if "csv" not in content_type.lower():
                raise ValueError(f"{node_id}: expected CSV, got {content_type!r}")
            with csv_path.open("wb") as out:
                for chunk in resp.iter_bytes(CHUNK_SIZE):
                    if chunk:
                        out.write(chunk)

        with duckdb.connect(":memory:") as conn:
            conn.execute(
                """
                COPY (
                    SELECT *
                    FROM read_csv_auto(?, header = true, sample_size = -1)
                )
                TO ? (FORMAT PARQUET, COMPRESSION ZSTD)
                """,
                [str(csv_path), str(parquet_path)],
            )

        with raw_writer(node_id, extension="parquet", mode="wb") as out:
            with parquet_path.open("rb") as src:
                while chunk := src.read(CHUNK_SIZE):
                    if chunk:
                        out.write(chunk)


DOWNLOAD_SPECS = [
    NodeSpec(id="stats19-collisions", fn=fetch_csv, kind="download"),
    NodeSpec(id="stats19-vehicles", fn=fetch_csv, kind="download"),
    NodeSpec(id="stats19-casualties", fn=fetch_csv, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "DfT says final STATS19 open data is released annually in late "
            "September, with provisional half-year data in November; complete "
            "validated history is refreshed on that cadence per "
            "https://www.gov.uk/government/statistical-data-sets/road-safety-open-data."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "parquet", max_age_days=30),
    )
    for spec in DOWNLOAD_SPECS
]
