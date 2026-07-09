"""CSO Ireland (PxStat) — one download node per PxStat matrix.

Each matrix is fetched in full from a single stable ReadDataset URL
(`.../ReadDataset/{matrix}/CSV/1.0/en`): no pagination, no delta filter, so
every node is a stateless full re-pull and revisions are picked up for free.

The source CSV is a flat cell-per-row export whose *column set* differs per
matrix: one (code, label) column pair per dimension — exactly one of which is
`STATISTIC` and exactly one the time dimension `TLIST(<freq>1)` — followed by
`UNIT` and `VALUE`. Fetch normalizes that into one schema shared by all assets:
statistic and time are lifted into named columns, the remaining dimensions are
slotted into `dim1..dim6` (dimension name / category code / category label), and
the PxStat time code is resolved to real `period_start` / `period_end` dates so
downstream never has to re-derive each matrix's time encoding.

No MAINTAIN_SPECS: the only per-matrix freshness signal the source offers is the
`updated` field on the catalog endpoint, and consulting it would mean ~10k HEAD
requests in the orchestrator's parent process before every run. Refresh cadence
is owned by maintenance.json instead.
"""

import csv
import datetime
import io
import re
import time

import pyarrow as pa
from constants import ENTITY_IDS
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    save_state,
    transient_retry,
)

SLUG = "central-statistics-office"
DATASET_URL = (
    "https://ws.cso.ie/public/api.restful/"
    "PxStat.Data.Cube_API.ReadDataset/{matrix}/CSV/1.0/en"
)

STATE_VERSION = 1
SKIP_TTL_SECONDS = 14 * 86400

# n_dimensions tops out at 8 across the catalog; STATISTIC and time take two.
MAX_DIMS = 6

_TLIST = re.compile(r"^TLIST\(([A-Z])\d\)$")

SCHEMA = pa.schema(
    [
        ("matrix", pa.string()),
        ("statistic_code", pa.string()),
        ("statistic_label", pa.string()),
        ("time_code", pa.string()),
        ("time_label", pa.string()),
        ("time_dimension", pa.string()),
        ("period_start", pa.date32()),
        ("period_end", pa.date32()),
        ("unit", pa.string()),
        ("value", pa.float64()),
    ]
    + [
        (f"dim{slot}_{part}", pa.string())
        for slot in range(1, MAX_DIMS + 1)
        for part in ("name", "code", "label")
    ]
)
SCHEMA_FIELDS = [(f.name, f.type) for f in SCHEMA]

# PxStat time codes are not uniform even within one TLIST frequency: TLIST(W1)
# carries 'W01', '2019W01' and '2023M01D02' across different matrices. Match on
# the code's own shape, and consult the frequency letter only to break the
# YYYYQ / YYYYH tie, which is genuinely ambiguous.
_DAY = re.compile(r"^(\d{4})M(\d{2})D(\d{2})$")
_YMD = re.compile(r"^(\d{4})(\d{2})(\d{2})$")
_MONTH = re.compile(r"^(\d{4})M(\d{2})$")
_YM = re.compile(r"^(\d{4})(\d{2})$")
_WEEK = re.compile(r"^(\d{4})W(\d{2})$")
_QUARTER = re.compile(r"^(\d{4})Q(\d)$")
_HALF = re.compile(r"^(\d{4})H(\d)$")
_YEAR_PERIOD = re.compile(r"^(\d{4})(\d)$")
_SEASON = re.compile(r"^(\d{4})\d{4}$")
_YEAR_SLASH = re.compile(r"^(\d{4})/\d{2}$")
_YEAR = re.compile(r"^(\d{4})$")


def _month_span(year: int, month: int, months: int):
    """Calendar span covering `months` months starting at year-month."""
    start = datetime.date(year, month, 1)
    end = month + months - 1
    end_year, end_month = year + (end - 1) // 12, (end - 1) % 12 + 1
    if end_month == 12:
        next_start = datetime.date(end_year + 1, 1, 1)
    else:
        next_start = datetime.date(end_year, end_month + 1, 1)
    return start, next_start - datetime.timedelta(days=1)


def parse_period(code: str, freq: str):
    """(period_start, period_end) for a PxStat time code, or (None, None).

    Year-less codes ('W01' — a week-of-year profile averaged across several
    years) name no calendar period and resolve to (None, None) by design.
    """
    code = (code or "").strip()

    match = _DAY.match(code) or _YMD.match(code)
    if match:
        try:
            day = datetime.date(int(match[1]), int(match[2]), int(match[3]))
        except ValueError:
            return None, None
        return day, day

    match = _MONTH.match(code) or (_YM.match(code) if len(code) == 6 else None)
    if match and 1 <= int(match[2]) <= 12:
        return _month_span(int(match[1]), int(match[2]), 1)

    match = _WEEK.match(code)
    if match and 1 <= int(match[2]) <= 53:
        try:
            start = datetime.date.fromisocalendar(int(match[1]), int(match[2]), 1)
        except ValueError:
            return None, None
        return start, start + datetime.timedelta(days=6)

    match = _QUARTER.match(code)
    if match and 1 <= int(match[2]) <= 4:
        return _month_span(int(match[1]), 3 * int(match[2]) - 2, 3)

    match = _HALF.match(code)
    if match and 1 <= int(match[2]) <= 2:
        return _month_span(int(match[1]), 6 * int(match[2]) - 5, 6)

    match = _YEAR_PERIOD.match(code)
    if match:
        period = int(match[2])
        if freq == "Q" and 1 <= period <= 4:
            return _month_span(int(match[1]), 3 * period - 2, 3)
        if freq == "H" and 1 <= period <= 2:
            return _month_span(int(match[1]), 6 * period - 5, 6)
        return None, None

    # A season or academic span ('20112012', '2012/17'): the code names a
    # multi-year window whose start year is the only reliable anchor.
    match = _SEASON.match(code) or _YEAR_SLASH.match(code) or _YEAR.match(code)
    if match and 1800 <= int(match[1]) <= 2200:
        return _month_span(int(match[1]), 1, 12)

    return None, None


def _to_float(raw: str):
    raw = (raw or "").strip()
    if not raw:
        return None
    return float(raw)


@transient_retry()
def _fetch_csv(matrix: str):
    """The decoded CSV body, or None when PxStat no longer serves the matrix."""
    resp = get(DATASET_URL.format(matrix=matrix), timeout=(10.0, 300.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.content.decode("utf-8-sig")


def _parse(matrix: str, text: str) -> pa.Table:
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    if header[-2:] != ["UNIT", "VALUE"]:
        raise ValueError(f"{matrix}: expected trailing UNIT,VALUE columns, got {header[-2:]}")

    pairs = [(header[i], header[i + 1], i) for i in range(0, len(header) - 2, 2)]
    statistic = next((p for p in pairs if p[0] == "STATISTIC"), None)
    if statistic is None:
        raise ValueError(f"{matrix}: no STATISTIC dimension in {header}")
    stamps = [p for p in pairs if _TLIST.match(p[0])]
    if len(stamps) != 1:
        raise ValueError(f"{matrix}: expected one TLIST column, got {[p[0] for p in stamps]}")
    stamp = stamps[0]
    freq = _TLIST.match(stamp[0])[1]
    others = [p for p in pairs if p is not statistic and p is not stamp]
    if len(others) > MAX_DIMS:
        raise ValueError(f"{matrix}: {len(others)} extra dimensions exceeds MAX_DIMS={MAX_DIMS}")

    cols = {name: [] for name, _ in SCHEMA_FIELDS}
    spans: dict[str, tuple] = {}

    for row in reader:
        if not row:
            continue
        code = row[stamp[2]]
        if code not in spans:
            spans[code] = parse_period(code, freq)
        start, end = spans[code]

        cols["matrix"].append(matrix)
        cols["statistic_code"].append(row[statistic[2]])
        cols["statistic_label"].append(row[statistic[2] + 1])
        cols["time_code"].append(code)
        cols["time_label"].append(row[stamp[2] + 1])
        cols["time_dimension"].append(stamp[1])
        cols["period_start"].append(start)
        cols["period_end"].append(end)
        cols["unit"].append(row[-2])
        cols["value"].append(_to_float(row[-1]))

        for slot in range(1, MAX_DIMS + 1):
            if slot <= len(others):
                code_col, name, idx = others[slot - 1]
                cols[f"dim{slot}_name"].append(name)
                cols[f"dim{slot}_code"].append(row[idx])
                cols[f"dim{slot}_label"].append(row[idx + 1])
            else:
                cols[f"dim{slot}_name"].append(None)
                cols[f"dim{slot}_code"].append(None)
                cols[f"dim{slot}_label"].append(None)

    return pa.table(
        {name: pa.array(cols[name], type=typ) for name, typ in SCHEMA_FIELDS},
        schema=SCHEMA,
    )


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    matrix = node_id.removeprefix(f"{SLUG}-").upper()

    text = _fetch_csv(matrix)
    if text is None:
        # Permanent: an accepted matrix PxStat has stopped serving. Skip this one
        # entity rather than failing the node, and let the marker expire so a
        # restored table is picked up again without a human.
        save_state(
            asset,
            {
                "schema_version": STATE_VERSION,
                "skipped": {
                    "reason": f"ReadDataset returned 404 for matrix {matrix}",
                    "expires_at": int(time.time()) + SKIP_TTL_SECONDS,
                },
            },
        )
        return

    save_raw_parquet(_parse(matrix, text), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
