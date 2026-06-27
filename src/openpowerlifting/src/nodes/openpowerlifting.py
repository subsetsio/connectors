"""OpenPowerlifting connector — the full powerlifting meet-results corpus.

Single entity (`results`): OpenPowerlifting publishes its entire database nightly
as one zipped, fully-denormalized CSV (one row per lifter-per-meet, ~3.96M rows)
at a stable URL, no auth, no incremental-query parameter. The whole corpus is
~166MB zipped, so the correct shape is a **stateless full re-pull**: re-fetch the
zip every run and overwrite — revisions and late corrections are picked up for
free because no watermark is trusted.

Raw is streamed CSV -> parquet with every column kept as a string. The CSV mixes
numeric values with sentinels ('DQ'/'NS'/'G' in Place, '+' in WeightClassKg,
negative weights for failed attempts, 'n.5' approximate ages), so typing is left
entirely to the transform, which TRY_CASTs the columns it publishes.
"""
import csv
import io
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
)

RESULTS_URL = "https://openpowerlifting.gitlab.io/opl-csv/files/openpowerlifting-latest.zip"


@transient_retry()
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def fetch_results(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    zf = zipfile.ZipFile(io.BytesIO(_download(RESULTS_URL)))
    csv_members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
    if len(csv_members) != 1:
        raise AssertionError(
            f"expected exactly 1 CSV inside the zip, found {csv_members}"
        )
    member = csv_members[0]

    # Read the header to pin an all-string schema; keep every published column as
    # VARCHAR and let the transform cast. Robust to the CSV's mixed sentinels.
    with zf.open(member) as fh:
        header = next(csv.reader(io.TextIOWrapper(fh, encoding="utf-8")))
    schema = pa.schema([(c, pa.string()) for c in header])

    read_opts = pacsv.ReadOptions(block_size=64 << 20)
    convert_opts = pacsv.ConvertOptions(
        column_types={c: pa.string() for c in header}
    )
    with zf.open(member) as fh:
        reader = pacsv.open_csv(
            fh, read_options=read_opts, convert_options=convert_opts
        )
        with raw_parquet_writer(asset, schema) as writer:
            for batch in reader:
                writer.write_table(pa.Table.from_batches([batch], schema=schema))


DOWNLOAD_SPECS = [
    NodeSpec(id="openpowerlifting-results", fn=fetch_results, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openpowerlifting-results-transform",
        deps=["openpowerlifting-results"],
        sql='''
            SELECT
                "Name"                                        AS name,
                "Sex"                                         AS sex,
                "Event"                                       AS event,
                "Equipment"                                   AS equipment,
                NULLIF("Place", '')                           AS place,
                NULLIF("Division", '')                        AS division,
                TRY_CAST("Age" AS DOUBLE)                     AS age,
                NULLIF("AgeClass", '')                        AS age_class,
                NULLIF("BirthYearClass", '')                  AS birth_year_class,
                TRY_CAST("BodyweightKg" AS DOUBLE)            AS bodyweight_kg,
                NULLIF("WeightClassKg", '')                   AS weight_class_kg,
                TRY_CAST("Best3SquatKg" AS DOUBLE)            AS best3_squat_kg,
                TRY_CAST("Best3BenchKg" AS DOUBLE)            AS best3_bench_kg,
                TRY_CAST("Best3DeadliftKg" AS DOUBLE)         AS best3_deadlift_kg,
                TRY_CAST("TotalKg" AS DOUBLE)                 AS total_kg,
                TRY_CAST("Dots" AS DOUBLE)                    AS dots,
                TRY_CAST("Wilks" AS DOUBLE)                   AS wilks,
                TRY_CAST("Glossbrenner" AS DOUBLE)            AS glossbrenner,
                TRY_CAST("Goodlift" AS DOUBLE)                AS goodlift,
                -- OPL sets Tested='Yes' only for drug-tested categories; blank
                -- means the lifter did NOT enter a tested category. Map blank to
                -- FALSE so this is a clean, fully-populated boolean.
                ("Tested" = 'Yes')                            AS tested,
                NULLIF("Country", '')                         AS country,
                NULLIF("State", '')                           AS state,
                "Federation"                                  AS federation,
                NULLIF("ParentFederation", '')                AS parent_federation,
                TRY_CAST("Date" AS DATE)                      AS date,
                "MeetCountry"                                 AS meet_country,
                NULLIF("MeetState", '')                       AS meet_state,
                NULLIF("MeetTown", '')                        AS meet_town,
                "MeetName"                                    AS meet_name
            FROM "openpowerlifting-results"
        ''',
    ),
]
