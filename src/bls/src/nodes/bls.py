"""BLS connector — bulk flat-file time series, one raw asset per survey database.

Mechanism: `bulk_flatfiles` (research's chosen surface). Every survey database under
https://download.bls.gov/pub/time.series/<survey>/ exposes its entire corpus as a
handful of stable-URL, tab-delimited flat files — no auth, no pagination, no
per-series request. A survey directory holds:

  <survey>.data.N.<slice>   long-format observations: series_id, year, period, value,
                            footnote_codes (the 5-column header is identical across
                            all 35 surveys)
  <survey>.series           the series catalog: series_id + that survey's dimension
                            code columns + series_title + the series' begin/end period
  <survey>.<dimension>      code -> label maps (e.g. cu.area, ce.industry, jt.seasonal)

Per survey we fetch all three kinds, join them in DuckDB, and write ONE denormalized
parquet asset: an observation per row, carrying its series' dimension codes, the
decoded dimension labels, and the series title. Nothing downstream can recover the
labels if we don't pull the code maps here, so we pull them here.

Fetch shape: stateless full re-pull (shape 1). The flat files carry no incremental
delta filter, so each refresh re-fetches the whole corpus and overwrites the asset;
revisions and late corrections are picked up for free. MAINTAIN_SPECS skips a survey
whose `<survey>.series` file is byte-identical to the one behind our last successful
fetch, which is what keeps the ~9GB corpus from being re-pulled on every tick.

Which data files to read: we read EVERY `<survey>.data.*` file and dedup, rather than
guessing a canonical one from its name. The names do not carry a reliable convention —
`ce.data.0.AllCESSeries` is the full corpus while `cu.data.1.AllItems` is the CPI
series for the *item* "All items", a 2.7MB slice of a 137MB survey; `<survey>.data.0.Current`
is a recent-years subset of the rest; and the LAUS per-state files overlap its
County/City/AllStates files. Slices are always subsets of the union, and duplicate rows
are byte-identical, so the union + DISTINCT is exact where any naming rule is a guess.
The cost is re-downloading the overlap (~9GB across the corpus instead of ~5GB).

CRITICAL AUTH QUIRK: download.bls.gov returns HTTP 403 to the default/empty
User-Agent. A descriptive User-Agent (incl. a contact email, ASCII only) is mandatory
on every request — including the HEAD probes MAINTAIN_SPECS makes.
"""
import os
import re
import tempfile

import duckdb

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    configure_http,
    get_client,
    raw_asset_exists,
    raw_parquet_writer,
    record_source_signature,
    source_unchanged,
    transient_retry,
)

# The entity union — the accepted BLS survey databases (work/entity_union.json).
from constants import ENTITY_IDS

_BASE = "https://download.bls.gov/pub/time.series"
# download.bls.gov 403s the default UA; a descriptive UA (with contact) is required.
_USER_AGENT = "subsets.io data connector (contact: nathansnellaert@gmail.com)"

# Series-catalog columns that describe the catalog row rather than the series: the
# observation rows carry their own footnote_codes, and begin/end period is derivable.
_SERIES_DROP = {"footnote_codes", "begin_year", "begin_period", "end_year", "end_period"}

# `eb.series` ends its header row with a stray tab, so DuckDB invents a `column7` for
# the unnamed trailing field. An unnamed source column is not a dimension.
_UNNAMED = re.compile(r"^column\d+$")

# The series catalog is the survey's series universe. Every survey we probed ships an
# observation for every catalogued series; a large shortfall means we lost a data file,
# which is exactly the silent partial load this guard exists to turn into a failure.
_MIN_SERIES_COVERAGE = 0.90

# BLS flat files are tab-delimited with whitespace-padded fields, CRLF line ends, and
# unescaped double quotes inside series titles — so quoting must be disabled outright.
_READ_CSV = "delim='\\t', header=true, quote='', escape='', all_varchar=true, null_padding=true"

_BATCH_ROWS = 100_000
_DUCKDB_MEMORY_LIMIT = "4GB"


def _use_bls_user_agent() -> None:
    """Idempotent; safe in both the fetch child and the maintain parent process."""
    configure_http(headers={"User-Agent": _USER_AGENT})


@transient_retry()
def _list_survey_files(survey: str) -> list[str]:
    """Every file name in the survey's HTML directory listing (basenames, not URLs)."""
    resp = get_client().get(f"{_BASE}/{survey}/", timeout=(10.0, 120.0))
    resp.raise_for_status()
    hrefs = re.findall(r'<A HREF="([^"]+)">', resp.text, flags=re.IGNORECASE)
    names = sorted({h.rsplit("/", 1)[-1] for h in hrefs if f"/{survey}." in h})
    if not names:
        raise AssertionError(f"{survey}: directory listing exposed no {survey}.* files")
    return names


@transient_retry()
def _download(survey: str, name: str, dest_dir: str) -> str:
    """Stream one flat file to scratch disk. Bounded memory: fw's data file is 622MB."""
    path = os.path.join(dest_dir, name)
    with get_client().stream("GET", f"{_BASE}/{survey}/{name}", timeout=(10.0, 900.0)) as resp:
        resp.raise_for_status()
        with open(path, "wb") as fh:
            for chunk in resp.iter_bytes(1 << 20):
                fh.write(chunk)
    return path


def _columns(con: duckdb.DuckDBPyConnection, path: str) -> list[str]:
    return [r[0] for r in con.execute(f"DESCRIBE SELECT * FROM read_csv('{path}', {_READ_CSV})").fetchall()]


def _label_column(header: list[str]) -> str | None:
    """The map file's human-readable column: the first `*_name` / `*_text` after the key."""
    for col in header[1:]:
        if col.endswith(("_name", "_text")):
            return col
    return None


def _decodable_maps(con, survey, names, dest_dir, dims) -> dict[str, tuple[str, str, str]]:
    """Pick the code -> label maps we can join without changing the observation grain.

    Only single-column keys qualify: a map whose first column is the series column we
    would join on. `la.area` is keyed on (area_type_code, area_code) and `oe.area` on
    (state_code, area_code, areatype_code), so joining either on area_code alone would
    fan rows out — those are skipped, and their codes ship undecoded.

    Returns {series_column: (map_path, key_column, label_column)}.
    """
    maps: dict[str, tuple[str, str, str]] = {}
    emitted: set[str] = set()
    for col in dims:
        stem = col[:-5] if col.endswith("_code") else col
        name = f"{survey}.{stem}"
        if name not in names:
            continue
        out = f"{stem}_name"
        if out in dims or out in emitted:
            continue
        path = _download(survey, name, dest_dir)
        header = _columns(con, path)
        if not header or header[0] not in (col, f"{stem}_code"):
            continue
        label = _label_column(header)
        if label is None:
            continue
        key = header[0]
        unique = con.execute(
            f"SELECT count(*) = count(DISTINCT trim({key})) FROM read_csv('{path}', {_READ_CSV})"
        ).fetchone()[0]
        if not unique:
            continue
        maps[col] = (path, key, label)
        emitted.add(out)
    return maps


def _dimension_columns(series_cols: list[str]) -> list[str]:
    return [c for c in series_cols
            if c != "series_id" and c not in _SERIES_DROP and not _UNNAMED.match(c)]


def _build_query(survey, data_paths, series_path, series_cols, maps) -> str:
    """Observations x their series x the decodable dimension labels, one row per obs."""
    dims = _dimension_columns(series_cols)

    selects = [
        "o.series_id",
        "o.year",
        "o.period",
        # M13 / Q05 / S03 / A01 are annual aggregates; they land on Jan 1 and `period`
        # is what distinguishes them from the January / Q1 / H1 observation.
        """CASE
            WHEN o.period BETWEEN 'M01' AND 'M12'
                THEN make_date(o.year, CAST(substr(o.period, 2, 2) AS INTEGER), 1)
            WHEN o.period BETWEEN 'Q01' AND 'Q04'
                THEN make_date(o.year, (CAST(substr(o.period, 2, 2) AS INTEGER) - 1) * 3 + 1, 1)
            WHEN o.period = 'S02' THEN make_date(o.year, 7, 1)
            ELSE make_date(o.year, 1, 1)
        END AS period_start_date""",
        "o.value",
        "o.footnote_codes",
    ]
    joins = []
    for i, col in enumerate(dims):
        selects.append(f"s.{col}")
        if col in maps:
            path, key, label = maps[col]
            stem = col[:-5] if col.endswith("_code") else col
            selects.append(f'm{i}."{label}" AS {stem}_name')
            joins.append(
                f"LEFT JOIN (SELECT trim({key}) AS k, nullif(trim(\"{label}\"), '') AS \"{label}\" "
                f"FROM read_csv('{path}', {_READ_CSV})) m{i} ON m{i}.k = s.{col}"
            )

    series_selects = ", ".join(
        [f"trim(series_id) AS series_id"]
        + [f"nullif(trim({c}), '') AS {c}" for c in dims]
    )
    return f"""
        WITH obs AS (
            SELECT DISTINCT
                trim(series_id) AS series_id,
                TRY_CAST(trim(year) AS INTEGER) AS year,
                trim(period) AS period,
                TRY_CAST(trim(value) AS DOUBLE) AS value,
                nullif(trim(footnote_codes), '') AS footnote_codes
            FROM read_csv({data_paths!r}, {_READ_CSV}, union_by_name=true)
            WHERE trim(year) SIMILAR TO '[0-9]+'
        ),
        ser AS (
            SELECT {series_selects} FROM read_csv('{series_path}', {_READ_CSV})
        )
        SELECT {", ".join(selects)}
        FROM obs o
        LEFT JOIN ser s ON s.series_id = o.series_id
        {" ".join(joins)}
    """


def fetch_one(node_id: str) -> None:
    """Fetch one survey database: all observation files, its series catalog, its code maps."""
    _use_bls_user_agent()
    asset = node_id                       # the spec id IS the asset name
    survey = node_id[len("bls-"):]        # recover the survey abbreviation

    names = _list_survey_files(survey)
    data_files = [n for n in names if n.startswith(f"{survey}.data.")]
    if not data_files:
        raise AssertionError(f"{survey}: directory listing exposed no {survey}.data.* files")
    if f"{survey}.series" not in names:
        raise AssertionError(f"{survey}: directory listing exposed no {survey}.series catalog")

    with tempfile.TemporaryDirectory() as scratch:
        data_paths = [_download(survey, n, scratch) for n in data_files]
        series_path = _download(survey, f"{survey}.series", scratch)

        con = duckdb.connect()
        con.execute(f"SET memory_limit='{_DUCKDB_MEMORY_LIMIT}'")
        con.execute(f"SET temp_directory='{scratch}'")
        con.execute("SET preserve_insertion_order=false")

        series_cols = _columns(con, series_path)
        dims = _dimension_columns(series_cols)
        maps = _decodable_maps(con, survey, names, scratch, dims)

        catalogued, observed = con.execute(f"""
            SELECT
                (SELECT count(DISTINCT trim(series_id)) FROM read_csv('{series_path}', {_READ_CSV})),
                (SELECT count(DISTINCT trim(series_id))
                 FROM read_csv({data_paths!r}, {_READ_CSV}, union_by_name=true))
        """).fetchone()
        print(f"  {survey}: {len(data_files)} data file(s), {catalogued} catalogued series, "
              f"{observed} observed, {len(maps)}/{len(dims)} dimensions decoded")
        if catalogued and observed < catalogued * _MIN_SERIES_COVERAGE:
            raise AssertionError(
                f"{survey}: observations cover only {observed} of {catalogued} catalogued series "
                f"(< {_MIN_SERIES_COVERAGE:.0%}) — a data file is missing from the union"
            )

        reader = con.execute(_build_query(survey, data_paths, series_path, series_cols, maps)) \
                    .fetch_record_batch(_BATCH_ROWS)
        with raw_parquet_writer(asset, reader.schema) as writer:
            for batch in reader:
                writer.write_batch(batch)

    record_source_signature(asset, f"{_BASE}/{survey}/{survey}.series")


def _survey_unchanged(asset_id: str) -> bool:
    """True when the survey's series catalog hasn't been rewritten since our last fetch.

    BLS rewrites every file in a survey directory on each release, so the catalog's
    ETag is a proxy for "this survey published nothing new".
    """
    _use_bls_user_agent()
    survey = asset_id[len("bls-"):]
    return (source_unchanged(asset_id, f"{_BASE}/{survey}/{survey}.series")
            and raw_asset_exists(asset_id, "parquet"))


DOWNLOAD_SPECS = [
    NodeSpec(id=f"bls-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Re-fetched whenever <survey>.series changes (ETag/Last-Modified). BLS release "
            "cadence is per-survey, monthly to annual, published at "
            "https://www.bls.gov/schedule/news_release/"
        ),
        check=_survey_unchanged,
    )
    for spec in DOWNLOAD_SPECS
]
