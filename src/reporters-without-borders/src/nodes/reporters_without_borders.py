"""Reporters Without Borders — World Press Freedom Index.

Single statistical product: RSF's annual, comparative press-freedom assessment of
~180 countries/territories. One Delta table, one row per country-year.

Mechanism (chosen: bulk_csv): one semicolon-delimited CSV per index year at the
stable template https://rsf.org/sites/default/files/import_classement/<year>.csv .
Files are UTF-8-with-BOM, decimal comma. RSF published an index every year from
2002 onward EXCEPT 2011 (that file resolves but is empty). The period set is
DISCOVERED at fetch time by probing each year from the documented start (2002)
through the current calendar year and keeping the files that carry data, so a
newly-published year is picked up automatically with no code change.

Two methodology eras share the same overall Score/Rank/ISO/Year/Zone columns:
  * old (2002-2021): header 'Year (N);ISO;Rank N;Score N;...;EN_country;Zone';
    overall score only, on the older point scale.
  * new (2022+): header 'ISO;Score[ <year>];Rank;Political Context;Rank_Pol;...
    Safety;Rank_Saf;Zone;Country_EN;...;Year (N);Rank N-1;...'; adds five 0-100
    sub-indicator scores (Political/Economic/Legal/Social Context + Safety) with
    per-indicator ranks. Sub-indicators are nullable for the pre-2022 rows.

Stateless full re-pull: the whole corpus is a few hundred KB, so every run
re-fetches all years and overwrites — revisions and late corrections are picked
up for free. No watermark/cursor.
"""

import csv
import io
import re
from datetime import datetime, timezone

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

BASE = "https://rsf.org/sites/default/files/import_classement/{year}.csv"
MIN_YEAR = 2002  # documented first World Press Freedom Index

# Raw schema — declared once, the contract for the single parquet asset.
SCHEMA = pa.schema([
    ("iso", pa.string()),
    ("country", pa.string()),
    ("year", pa.int32()),
    ("score", pa.float64()),
    ("rank", pa.int32()),
    ("zone", pa.string()),
    ("political_context", pa.float64()),
    ("rank_pol", pa.int32()),
    ("economic_context", pa.float64()),
    ("rank_eco", pa.int32()),
    ("legal_context", pa.float64()),
    ("rank_leg", pa.int32()),
    ("social_context", pa.float64()),
    ("rank_soc", pa.int32()),
    ("safety", pa.float64()),
    ("rank_saf", pa.int32()),
    ("rank_prev", pa.int32()),
    ("rank_evolution", pa.int32()),
    ("score_prev", pa.float64()),
    ("score_evolution", pa.float64()),
    ("methodology_era", pa.string()),
    ("score_scale", pa.string()),
])

# RSF's overall-score scale flips at 2013 (verified: sign of corr(score, rank)
# flips). 2002-2012 use a legacy point system where LOWER is better (best
# countries go negative, worst ~140); 2013 onward use a 0-100 index where HIGHER
# is better. The two are NOT comparable, so the scale is published as a column.
def _score_scale(file_year: int) -> str:
    return "legacy_points_lower_better" if file_year <= 2012 else "index_0_100_higher_better"

_SCORE_RE = re.compile(r"^Score(?: \d{4})?$")  # new-era main score: "Score" or "Score 2026"


@transient_retry()
def _fetch_year(year: int) -> bytes | None:
    """Return CSV bytes for a year, or None if RSF published no index that year
    (404, or the 200-with-empty-body case that 2011 exhibits)."""
    resp = get(BASE.format(year=year), timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    content = resp.content
    return content if content and content.strip() else None


def _num(raw):
    """Decimal-comma string -> float, or None when blank."""
    if raw is None:
        return None
    s = raw.strip().replace(",", ".")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _intnum(raw):
    f = _num(raw)
    return int(round(f)) if f is not None else None


def _pick(row, *names):
    for n in names:
        if n in row:
            return row[n]
    return None


def _parse_row(row: dict, fieldnames: list[str], new_era: bool, file_year: int) -> dict | None:
    iso = (_pick(row, "ISO") or "").strip()
    if not iso:
        return None  # skip any aggregate/blank rows (none observed, but be safe)

    # Year is taken from the file we fetched, not the in-file "Year (N)" column:
    # the columns agree for every year EXCEPT 2012.csv, which is RSF's combined
    # "2011-12" edition (non-numeric "Year (N)"). Anchoring to the filename keeps
    # year non-null and maps that combined edition to 2012.
    if new_era:
        score_col = next((f for f in fieldnames if _SCORE_RE.match(f)), None)
        score = _num(row.get(score_col)) if score_col else None
        return {
            "iso": iso,
            "country": (_pick(row, "Country_EN") or "").strip() or None,
            "year": file_year,
            "score": score,
            "rank": _intnum(_pick(row, "Rank")),
            "zone": (_pick(row, "Zone") or "").strip() or None,
            "political_context": _num(_pick(row, "Political Context")),
            "rank_pol": _intnum(_pick(row, "Rank_Pol")),
            "economic_context": _num(_pick(row, "Economic Context")),
            "rank_eco": _intnum(_pick(row, "Rank_Eco")),
            "legal_context": _num(_pick(row, "Legal Context")),
            "rank_leg": _intnum(_pick(row, "Rank_Leg")),
            "social_context": _num(_pick(row, "Social Context")),
            "rank_soc": _intnum(_pick(row, "Rank_Soc")),
            "safety": _num(_pick(row, "Safety")),
            "rank_saf": _intnum(_pick(row, "Rank_Saf")),
            "rank_prev": _intnum(_pick(row, "Rank N-1")),
            "rank_evolution": _intnum(_pick(row, "Rank evolution")),
            # score_prev / score_evolution only exist from 2026 on; absent -> None
            "score_prev": _num(_pick(row, "Score N-1")),
            "score_evolution": _num(_pick(row, "Score evolution")),
            "methodology_era": "new_2022",
            "score_scale": _score_scale(file_year),
        }

    # old era (2002-2021): overall score only
    return {
        "iso": iso,
        "country": (_pick(row, "EN_country") or "").strip() or None,
        "year": file_year,
        "score": _num(_pick(row, "Score N")),
        "rank": _intnum(_pick(row, "Rank N")),
        "zone": (_pick(row, "Zone") or "").strip() or None,
        "political_context": None,
        "rank_pol": None,
        "economic_context": None,
        "rank_eco": None,
        "legal_context": None,
        "rank_leg": None,
        "social_context": None,
        "rank_soc": None,
        "safety": None,
        "rank_saf": None,
        "rank_prev": _intnum(_pick(row, "Rank N-1")),
        "rank_evolution": _intnum(_pick(row, "Rank evolution")),
        # old-era "Score N-1" is unreliable (occasional sentinel values); leave null
        "score_prev": None,
        "score_evolution": None,
        "methodology_era": "old_pre2022",
        "score_scale": _score_scale(file_year),
    }


def fetch_index(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    current_year = datetime.now(tz=timezone.utc).year
    rows: list[dict] = []
    for year in range(MIN_YEAR, current_year + 1):
        content = _fetch_year(year)
        if content is None:
            continue  # no index published that year (e.g. 2011) or not yet released
        text = content.decode("utf-8-sig", errors="replace")
        reader = csv.DictReader(io.StringIO(text), delimiter=";")
        fieldnames = reader.fieldnames or []
        new_era = "Political Context" in fieldnames
        for raw_row in reader:
            parsed = _parse_row(raw_row, fieldnames, new_era, year)
            if parsed is not None:
                rows.append(parsed)

    if not rows:
        raise RuntimeError(
            f"{asset}: discovered no index years in {MIN_YEAR}-{current_year} — "
            "the CSV URL template or hosting likely changed"
        )

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


ENTITY_ID = "reporters-without-borders-world-press-freedom-index"

DOWNLOAD_SPECS = [
    NodeSpec(id=ENTITY_ID, fn=fetch_index, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{ENTITY_ID}-transform",
        deps=[ENTITY_ID],
        sql=f'''
            SELECT
                iso,
                country,
                CAST(year AS INTEGER)              AS year,
                CAST(score AS DOUBLE)              AS score,
                CAST(rank AS INTEGER)              AS rank,
                zone,
                political_context,
                rank_pol,
                economic_context,
                rank_eco,
                legal_context,
                rank_leg,
                social_context,
                rank_soc,
                safety,
                rank_saf,
                rank_prev,
                rank_evolution,
                score_prev,
                score_evolution,
                methodology_era,
                score_scale
            FROM "{ENTITY_ID}"
            WHERE iso IS NOT NULL
              AND year IS NOT NULL
              AND score IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY iso, year ORDER BY score DESC) = 1
        ''',
    ),
]
