"""Dartmouth Atlas of Health Care connector.

Mechanism: bulk_csv_longitudinal. Each entity is a topic published by the Atlas
as one or more zipped, tidy long-format CSVs (one file per geographic level and
era) under https://data.dartmouthatlas.org/downloads/. We fetch every file for
an entity, unzip in memory, normalize column names to a canonical schema, tag
each row with its geographic level (parsed from the filename), and save the
union as one NDJSON raw asset. A DuckDB SQL transform then types/cleans it into
one published Delta table per entity.

NDJSON is the right raw format here: column sets drift across geo levels and
eras within a topic (the modern files carry Race/Gender + observed/expected
detail that the legacy files lack, and the OE-ratio column is named differently
across files), so a fixed parquet schema would be brittle. We normalize keys in
Python and let the transform re-type on read.

Full re-pull every run (shape 1, stateless): the corpus is a frozen archive, so
there is no incremental filter and none is needed; freshness is the maintain
step's concern. Some files are large (the HSA/county end-of-life and discharge
files are 100-170MB zipped, ~1-2GB / tens of millions of rows decompressed), so
we DECOMPRESS EACH ZIP MEMBER AS A STREAM and write NDJSON incrementally via
raw_writer -- never accumulating the corpus in memory.
"""

import csv
import io
import json
import re
import zipfile

import pandas as pd

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    raw_writer,
    transient_retry,
)
from constants import BASE, FILES, SLUG, TOPIC_ENTITIES

_UA = "Mozilla/5.0 (compatible; subsets-data-connector/1.0)"

# Canonical column set for every TOPIC entity. Built explicitly for each row so
# all topic entities emit identical keys regardless of which columns the source
# file happened to carry -> one uniform transform works for all six.
_TOPIC_COLUMNS = [
    "geo_level", "geo_code", "geo_label", "geo_name", "population", "year",
    "race", "gender", "cohort", "measure_code", "measure_label", "short_label",
    "cohort_web_label", "observed", "crude_rate", "adjusted_rate", "expected",
    "expected_adjusted", "oe_ratio", "oe_adjusted_ratio", "std_error",
    "std_error_adjusted", "ci_upper", "ci_lower", "percentile",
]

_NA = {"", ".", "na", "n/a", "null", "none"}


def _entity_of(node_id: str) -> str:
    return node_id[len(SLUG) + 1:]


def _geo_level(filename: str) -> str:
    prefix = filename.split("_", 1)[0].lower()
    return {"hosp": "hospital"}.get(prefix, prefix)


def _s(v):
    if v is None:
        return None
    v = str(v).strip()
    return None if v.lower() in _NA else v


def _json_value(v):
    if v is None or pd.isna(v):
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, (int, float, str, bool)):
        return v
    return str(v)


def _clean_col(name) -> str:
    value = str(name or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return value or "unnamed"


def _year_from_filename(filename: str) -> int | None:
    match4 = re.search(r"(19|20)\d{2}", filename)
    if match4:
        return int(match4.group(0))
    match2 = re.search(r"(?:^|[^0-9])(\d{2})(?:_|[^0-9])", filename)
    if not match2:
        return None
    year = int(match2.group(1))
    return 2000 + year if year < 80 else 1900 + year


def _f(v):
    s = _s(v)
    if s is None:
        return None
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def _i(v):
    f = _f(v)
    return None if f is None else int(f)


@transient_retry()
def _download(url: str) -> bytes:
    """Download a .csv.zip into memory (retried). Decompression is local."""
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _iter_csv_rows(url: str):
    """Stream rows (lowercased-key dicts) from the CSV member of a .csv.zip.

    The zip member is decompressed as a stream so multi-GB files never fully
    materialize in memory."""
    zf = zipfile.ZipFile(io.BytesIO(_download(url)))
    members = [n for n in zf.namelist() if n.lower().endswith(".csv") and "__MACOSX" not in n]
    if not members:
        raise AssertionError(f"no CSV member in {url}: {zf.namelist()}")
    with zf.open(members[0]) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8-sig", errors="replace", newline="")
        for raw in csv.DictReader(text):
            yield {(k or "").strip().lstrip("﻿").lower(): val for k, val in raw.items()}


def _normalize_topic_row(r: dict, geo_level: str) -> dict:
    # OE ratio is named oe_ratio / o_e_ratio / oe_crude_ratio across files.
    oe_ratio = r.get("oe_ratio")
    if oe_ratio is None:
        oe_ratio = r.get("o_e_ratio")
    if oe_ratio is None:
        oe_ratio = r.get("oe_crude_ratio")
    return {
        "geo_level": geo_level,
        "geo_code": _s(r.get("geo_code")),
        "geo_label": _s(r.get("geo_label")),
        "geo_name": _s(r.get("geo_name")),
        "population": _i(r.get("population")),
        "year": _i(r.get("year")),
        "race": _s(r.get("race")),
        "gender": _s(r.get("gender")),
        "cohort": _s(r.get("cohort")),
        "measure_code": _s(r.get("eventname")),
        "measure_label": _s(r.get("event_label")),
        "short_label": _s(r.get("short_label")),
        "cohort_web_label": _s(r.get("cohort_web_label")),
        "observed": _f(r.get("observed")),
        "crude_rate": _f(r.get("crude_rate")),
        "adjusted_rate": _f(r.get("adjusted_rate")),
        "expected": _f(r.get("expected")),
        "expected_adjusted": _f(r.get("expected_adjusted")),
        "oe_ratio": _f(oe_ratio),
        "oe_adjusted_ratio": _f(r.get("oe_adjusted_ratio")),
        "std_error": _f(r.get("std_error")),
        "std_error_adjusted": _f(r.get("std_error_adjusted")),
        "ci_upper": _f(r.get("uppercl")),
        "ci_lower": _f(r.get("lowercl")),
        "percentile": _f(r.get("percentile")),
    }


def fetch_topic(node_id: str) -> None:
    """Fetch + normalize one topic entity (the six long-format rate tables).

    Streams every file's rows straight to a gzipped NDJSON raw asset."""
    configure_http(headers={"User-Agent": _UA})
    entity = _entity_of(node_id)
    written = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for rel in FILES[entity]:
            geo = _geo_level(rel.rsplit("/", 1)[-1])
            for r in _iter_csv_rows(BASE + rel):
                row = _normalize_topic_row(r, geo)
                if row["geo_code"] and row["year"] is not None and row["measure_code"]:
                    fh.write(json.dumps(row) + "\n")
                    written += 1
    if not written:
        raise AssertionError(f"{node_id}: zero rows after normalizing {len(FILES[entity])} files")


def fetch_crosswalk(node_id: str) -> None:
    """Fetch the ZIP -> HSA -> HRR geographic crosswalk (reference table).

    Each yearly file has its own zipcodeNN column; we normalize to `zipcode` and
    stamp each row with the file's `vintage` (the 4-digit year)."""
    configure_http(headers={"User-Agent": _UA})
    entity = _entity_of(node_id)
    written = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for rel in FILES[entity]:
            basename = rel.rsplit("/", 1)[-1]
            # ZipHsaHrr19.csv.zip -> vintage 2019
            digits = "".join(ch for ch in basename if ch.isdigit())
            vintage = 2000 + int(digits[-2:]) if digits else None
            for r in _iter_csv_rows(BASE + rel):
                zipcode = None
                for k, v in r.items():
                    if k.startswith("zipcode") or k == "zip":
                        zipcode = _s(v)
                        break
                if not zipcode:
                    continue
                fh.write(json.dumps({
                    "zipcode": zipcode,
                    "hsa_num": _i(r.get("hsanum")),
                    "hsa_city": _s(r.get("hsacity")),
                    "hsa_state": _s(r.get("hsastate")),
                    "hrr_num": _i(r.get("hrrnum")),
                    "hrr_city": _s(r.get("hrrcity")),
                    "hrr_state": _s(r.get("hrrstate")),
                    "vintage": vintage,
                }) + "\n")
                written += 1
    if not written:
        raise AssertionError(f"{node_id}: zero crosswalk rows")


def fetch_hospital_research_data(node_id: str) -> None:
    """Fetch hospital-level CSV bundles with drifty annual schemas."""
    configure_http(headers={"User-Agent": _UA})
    entity = _entity_of(node_id)
    written = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for rel in FILES[entity]:
            basename = rel.rsplit("/", 1)[-1]
            vintage = _year_from_filename(basename)
            for raw in _iter_csv_rows(BASE + rel):
                row = {
                    "source_file": basename,
                    "vintage": vintage,
                }
                for key, value in raw.items():
                    row[_clean_col(key)] = _s(value)
                fh.write(json.dumps(row) + "\n")
                written += 1
    if not written:
        raise AssertionError(f"{node_id}: zero hospital research rows")


def fetch_capacity_xls(node_id: str) -> None:
    """Fetch area-level hospital/physician capacity legacy XLS snapshots."""
    configure_http(headers={"User-Agent": _UA})
    entity = _entity_of(node_id)
    written = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for rel in FILES[entity]:
            basename = rel.rsplit("/", 1)[-1]
            geo_level = "hrr" if "_hrr" in basename else "hsa" if "_hsa" in basename else None
            vintage = _year_from_filename(basename)
            df = pd.read_excel(io.BytesIO(_download(BASE + rel)), sheet_name=0)
            df = df.dropna(how="all")
            for raw in df.to_dict(orient="records"):
                row = {
                    "source_file": basename,
                    "geo_level": geo_level,
                    "vintage": vintage,
                }
                for key, value in raw.items():
                    row[_clean_col(key)] = _json_value(value)
                fh.write(json.dumps(row) + "\n")
                written += 1
    if not written:
        raise AssertionError(f"{node_id}: zero capacity rows")


def fetch_mortality_stata(node_id: str) -> None:
    """Fetch mortality rates from direct Stata ZIPs; public CSV points to Dataverse."""
    configure_http(headers={"User-Agent": _UA})
    entity = _entity_of(node_id)
    written = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for rel in FILES[entity]:
            basename = rel.rsplit("/", 1)[-1]
            geo_level = _geo_level(basename)
            zf = zipfile.ZipFile(io.BytesIO(_download(BASE + rel)))
            members = [n for n in zf.namelist() if n.lower().endswith(".dta")]
            if not members:
                raise AssertionError(f"no DTA member in {rel}: {zf.namelist()}")
            with zf.open(members[0]) as member:
                df = pd.read_stata(io.BytesIO(member.read()), convert_categoricals=False)
            df = df.dropna(how="all")
            for raw in df.to_dict(orient="records"):
                row = {
                    "source_file": basename,
                    "geo_level": geo_level,
                }
                for key, value in raw.items():
                    row[_clean_col(key)] = _json_value(value)
                fh.write(json.dumps(row) + "\n")
                written += 1
    if not written:
        raise AssertionError(f"{node_id}: zero mortality rows")


def _spec_id(entity: str) -> str:
    return f"{SLUG}-{entity.lower().replace('_', '-')}"


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(e), fn=fetch_topic, kind="download") for e in TOPIC_ENTITIES
] + [
    NodeSpec(id=_spec_id("geography-crosswalk"), fn=fetch_crosswalk, kind="download"),
    NodeSpec(id=_spec_id("hospital-physician-capacity"), fn=fetch_capacity_xls, kind="download"),
    NodeSpec(id=_spec_id("hospital-research-data"), fn=fetch_hospital_research_data, kind="download"),
    NodeSpec(id=_spec_id("mortality"), fn=fetch_mortality_stata, kind="download"),
]


# ---------------------------------------------------------------------------
# Transforms — one published Delta table per entity
# ---------------------------------------------------------------------------

# SQL type per canonical column.
_COL_TYPE = {
    "geo_level": "VARCHAR", "geo_code": "VARCHAR", "geo_name": "VARCHAR",
    "cohort": "VARCHAR", "measure_code": "VARCHAR", "measure_label": "VARCHAR",
    "short_label": "VARCHAR", "cohort_web_label": "VARCHAR", "race": "VARCHAR",
    "gender": "VARCHAR", "year": "INTEGER", "population": "BIGINT",
    "adjusted_rate": "DOUBLE", "oe_ratio": "DOUBLE", "percentile": "DOUBLE",
    "observed": "DOUBLE", "crude_rate": "DOUBLE", "expected": "DOUBLE",
    "expected_adjusted": "DOUBLE", "oe_adjusted_ratio": "DOUBLE",
    "std_error": "DOUBLE", "std_error_adjusted": "DOUBLE",
    "ci_upper": "DOUBLE", "ci_lower": "DOUBLE",
}

# Columns every topic table carries.
_CORE_COLS = [
    "geo_level", "geo_code", "geo_name", "year", "population", "cohort",
    "measure_code", "measure_label", "short_label", "cohort_web_label",
    "adjusted_rate", "oe_ratio", "percentile",
]

# Columns BEYOND the core that each topic's source files actually populate.
# Anything not listed here is structurally absent for that topic (the Atlas ships
# different detail per topic) and is dropped so published tables carry no
# all-null columns. Derived from the source CSV headers.
_TOPIC_EXTRA = {
    "reimbursements": [],
    "end-of-life-inpatient-care": [
        "race", "gender", "observed", "crude_rate", "expected",
        "expected_adjusted", "oe_adjusted_ratio", "std_error",
        "std_error_adjusted", "ci_upper", "ci_lower",
    ],
    "care-chronically-ill-last-2yrs": ["observed", "crude_rate", "ci_upper", "ci_lower"],
    "primary-care-access-quality": [
        "race", "observed", "crude_rate", "std_error", "ci_upper", "ci_lower",
    ],
    "post-discharge-events": [
        "observed", "crude_rate", "expected", "expected_adjusted",
        "oe_adjusted_ratio", "std_error", "std_error_adjusted",
        "ci_upper", "ci_lower",
    ],
    "discharge-rates": [
        "race", "gender", "observed", "crude_rate", "expected_adjusted",
        "oe_adjusted_ratio", "std_error_adjusted", "ci_upper", "ci_lower",
    ],
}


# Columns to drop per topic even though they're "core": the source ships them
# but leaves them entirely empty for that topic.
_TOPIC_DROP = {
    "care-chronically-ill-last-2yrs": {"short_label", "cohort_web_label"},
}

# Dartmouth's missing/suppressed-value sentinel. The source writes -99999 (and
# -999999 for some columns) when a cell is suppressed; these must become NULL,
# NOT be treated as real measurements. Legitimate negative values exist (sparse
# risk-adjusted "Other_discharges" rates reach about -1800), so the cutoff sits
# safely below any real value and above the sentinels.
_SENTINEL_CUTOFF = -9999

# Numeric columns that carry the sentinel.
_NUMERIC = {"DOUBLE", "BIGINT"}


def _col_expr(c: str) -> str:
    t = _COL_TYPE[c]
    if t in _NUMERIC:
        # NULL out the suppression sentinel, keep real (incl. small-negative) values.
        return (
            f"CASE WHEN TRY_CAST({c} AS DOUBLE) <= {_SENTINEL_CUTOFF} "
            f"THEN NULL ELSE CAST({c} AS {t}) END AS {c}"
        )
    return f"CAST({c} AS {t}) AS {c}"


def _topic_sql(entity: str) -> str:
    dep = _spec_id(entity)
    drop = _TOPIC_DROP.get(entity, set())
    cols = [c for c in (_CORE_COLS + _TOPIC_EXTRA[entity]) if c not in drop]
    selects = ",\n            ".join(_col_expr(c) for c in cols)
    return f'''
        SELECT
            {selects}
        FROM "{dep}"
        WHERE geo_code IS NOT NULL
          AND year IS NOT NULL
          AND measure_code IS NOT NULL
    '''


_CROSSWALK_SQL = '''
    SELECT DISTINCT
        CAST(zipcode AS VARCHAR)  AS zipcode,
        CAST(hsa_num AS INTEGER)  AS hsa_num,
        CAST(hsa_city AS VARCHAR) AS hsa_city,
        CAST(hsa_state AS VARCHAR) AS hsa_state,
        CAST(hrr_num AS INTEGER)  AS hrr_num,
        CAST(hrr_city AS VARCHAR) AS hrr_city,
        CAST(hrr_state AS VARCHAR) AS hrr_state,
        CAST(vintage AS INTEGER)  AS vintage
    FROM "{dep}"
    WHERE zipcode IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{_spec_id(e)}-transform", deps=[_spec_id(e)], sql=_topic_sql(e))
    for e in TOPIC_ENTITIES
] + [
    SqlNodeSpec(
        id=f"{_spec_id('geography-crosswalk')}-transform",
        deps=[_spec_id("geography-crosswalk")],
        sql=_CROSSWALK_SQL.format(dep=_spec_id("geography-crosswalk")),
    ),
]
