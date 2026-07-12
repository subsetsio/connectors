"""Cricsheet connector — ball-by-ball cricket match data.

Mechanism: bulk_csv2 (the "Ashwin" CSV format). Cricsheet is a static file
server with stable, persistent zip URLs and no API/auth/rate-limit. We re-pull
the full corpus every run (stateless full re-pull — shape 1) because there is
no incremental query and the source is small enough (~120MB zip).

Three subsets, three distinct schemas:
  * cricsheet-deliveries — one row per delivery, from every <id>.csv in
    all_csv2.zip (identical 27-col header). Raw saved as all-string parquet,
    streamed batch-by-batch (~8-9M rows); the transform casts.
  * cricsheet-matches    — one row per match, pivoted from the long-format
    <id>_info.csv files in the same zip.
  * cricsheet-people     — the player/official identity register
    (people.csv); reference data joinable to deliveries by name.
"""

import collections
import csv
import io
import zipfile

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    raw_parquet_writer,
    save_raw_ndjson,
)

DELIVERIES_ZIP_URL = "https://cricsheet.org/downloads/all_csv2.zip"
PEOPLE_CSV_URL = "https://cricsheet.org/register/people.csv"

# Fixed ball-by-ball header of the csv2 ("Ashwin") format (verified, stable
# across the whole corpus). We map positionally to these names.
BALL_COLUMNS = [
    "match_id", "season", "start_date", "venue", "innings", "ball",
    "actual_delivery", "batting_team", "bowling_team", "striker",
    "non_striker", "bowler", "runs_off_bat", "extras", "wides", "noballs",
    "byes", "legbyes", "penalty", "non_boundary", "wicket_type",
    "player_dismissed", "other_wicket_type", "other_player_dismissed",
    "fielder_1", "fielder_2", "fielder_3",
]
DELIVERIES_SCHEMA = pa.schema([(c, pa.string()) for c in BALL_COLUMNS])
BATCH_ROWS = 250_000

# Single-valued info keys we lift verbatim into the wide matches row.
_INFO_SINGLE = [
    "balls_per_over", "team_type", "gender", "season", "event", "match_type",
    "match_number", "overs", "venue", "city", "toss_winner", "toss_decision",
    "player_of_match", "winner", "winner_runs", "winner_wickets", "method",
    "outcome",
]


def _download(url: str) -> bytes:
    # Generous read timeout: all_csv2.zip is ~120MB over a plain file server.
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _open_corpus_zip() -> zipfile.ZipFile:
    return zipfile.ZipFile(io.BytesIO(_download(DELIVERIES_ZIP_URL)))


def fetch_deliveries(node_id: str) -> None:
    asset = node_id
    z = _open_corpus_zip()
    ball_members = [
        n for n in z.namelist()
        if n.endswith(".csv") and not n.endswith("_info.csv")
    ]
    assert ball_members, "all_csv2.zip contained no ball-by-ball CSV files"

    with raw_parquet_writer(asset, DELIVERIES_SCHEMA) as writer:
        buf: list[list[str]] = []

        def flush() -> None:
            if not buf:
                return
            cols = list(zip(*buf))
            batch = pa.RecordBatch.from_arrays(
                [pa.array(c, type=pa.string()) for c in cols],
                names=BALL_COLUMNS,
            )
            writer.write_batch(batch)
            buf.clear()

        for name in ball_members:
            with z.open(name) as fh:
                reader = csv.reader(io.TextIOWrapper(fh, encoding="utf-8"))
                header = next(reader, None)
                if header is None:
                    continue
                assert header == BALL_COLUMNS, (
                    f"{name}: unexpected header {header!r}; csv2 format changed"
                )
                for row in reader:
                    if not row:
                        continue
                    if len(row) < len(BALL_COLUMNS):
                        row = row + [""] * (len(BALL_COLUMNS) - len(row))
                    elif len(row) > len(BALL_COLUMNS):
                        row = row[: len(BALL_COLUMNS)]
                    buf.append(row)
                    if len(buf) >= BATCH_ROWS:
                        flush()
        flush()


def fetch_matches(node_id: str) -> None:
    asset = node_id
    z = _open_corpus_zip()
    info_members = [n for n in z.namelist() if n.endswith("_info.csv")]
    assert info_members, "all_csv2.zip contained no _info.csv files"

    rows = []
    def iso_date(value: str | None) -> str | None:
        if not value:
            return None
        return value.replace("/", "-")

    for name in info_members:
        vals: dict[str, list[list[str]]] = collections.defaultdict(list)
        with z.open(name) as fh:
            for r in csv.reader(io.TextIOWrapper(fh, encoding="utf-8")):
                if len(r) >= 3 and r[0] == "info":
                    vals[r[1]].append(r[2:])

        def first(key: str):
            v = vals.get(key)
            return v[0][0] if v and v[0] else None

        teams = [t[0] for t in vals.get("team", []) if t]
        dates = sorted(d[0] for d in vals.get("date", []) if d)
        match_id = first("match_id") or name.rsplit("/", 1)[-1][: -len("_info.csv")]

        row = {k: first(k) for k in _INFO_SINGLE}
        row["match_id"] = match_id
        row["start_date"] = iso_date(dates[0]) if dates else None
        row["end_date"] = iso_date(dates[-1]) if dates else None
        row["team1"] = teams[0] if len(teams) > 0 else None
        row["team2"] = teams[1] if len(teams) > 1 else None
        rows.append(row)

    assert rows, "no match info rows parsed"
    save_raw_ndjson(rows, asset)


def fetch_people(node_id: str) -> None:
    asset = node_id
    text = _download(PEOPLE_CSV_URL).decode("utf-8")
    rows = [dict(r) for r in csv.DictReader(io.StringIO(text))]
    assert rows, "people.csv parsed to zero rows"
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="cricsheet-deliveries", fn=fetch_deliveries, kind="download"),
    NodeSpec(id="cricsheet-matches", fn=fetch_matches, kind="download"),
    NodeSpec(id="cricsheet-people", fn=fetch_people, kind="download"),
]
