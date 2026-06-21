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
import zipfile

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
def _fetch_zip_rows(url: str):
    """Download a .csv.zip, return (csv_basename, list[dict] with lowercased keys)."""
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(resp.content))
    members = [n for n in zf.namelist() if n.lower().endswith(".csv") and "__MACOSX" not in n]
    if not members:
        raise AssertionError(f"no CSV member in {url}: {zf.namelist()}")
    name = members[0]
    text = zf.read(name).decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for raw in reader:
        rows.append({(k or "").strip().lstrip("﻿").lower(): val for k, val in raw.items()})
    return name.rsplit("/", 1)[-1], rows


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
    """Fetch + normalize one topic entity (the six long-format rate tables)."""
    configure_http(headers={"User-Agent": _UA})
    entity = _entity_of(node_id)
    out = []
    for rel in FILES[entity]:
        basename = rel.rsplit("/", 1)[-1]
        geo = _geo_level(basename)
        _, rows = _fetch_zip_rows(BASE + rel)
        for r in rows:
            row = _normalize_topic_row(r, geo)
            if row["geo_code"] and row["year"] is not None and row["measure_code"]:
                out.append(row)
    if not out:
        raise AssertionError(f"{node_id}: zero rows after normalizing {len(FILES[entity])} files")
    save_raw_ndjson(out, node_id)


def fetch_crosswalk(node_id: str) -> None:
    """Fetch the ZIP -> HSA -> HRR geographic crosswalk (reference table).

    Each yearly file has its own zipcodeNN column; we normalize to `zipcode` and
    stamp each row with the file's `vintage` (the 4-digit year)."""
    configure_http(headers={"User-Agent": _UA})
    entity = _entity_of(node_id)
    out = []
    for rel in FILES[entity]:
        basename = rel.rsplit("/", 1)[-1]
        # ZipHsaHrr19.csv.zip -> vintage 2019
        digits = "".join(ch for ch in basename if ch.isdigit())
        vintage = 2000 + int(digits[-2:]) if digits else None
        _, rows = _fetch_zip_rows(BASE + rel)
        for r in rows:
            zipcode = None
            for k, v in r.items():
                if k.startswith("zipcode") or k == "zip":
                    zipcode = _s(v)
                    break
            out.append({
                "zipcode": zipcode,
                "hsa_num": _i(r.get("hsanum")),
                "hsa_city": _s(r.get("hsacity")),
                "hsa_state": _s(r.get("hsastate")),
                "hrr_num": _i(r.get("hrrnum")),
                "hrr_city": _s(r.get("hrrcity")),
                "hrr_state": _s(r.get("hrrstate")),
                "vintage": vintage,
            })
    out = [r for r in out if r["zipcode"]]
    if not out:
        raise AssertionError(f"{node_id}: zero crosswalk rows")
    save_raw_ndjson(out, node_id)


def _spec_id(entity: str) -> str:
    return f"{SLUG}-{entity.lower().replace('_', '-')}"


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(e), fn=fetch_topic, kind="download") for e in TOPIC_ENTITIES
] + [
    NodeSpec(id=_spec_id("geography-crosswalk"), fn=fetch_crosswalk, kind="download"),
]


# ---------------------------------------------------------------------------
# Transforms — one published Delta table per entity
# ---------------------------------------------------------------------------

def _topic_sql(dep: str) -> str:
    return f'''
        SELECT
            CAST(geo_level AS VARCHAR)         AS geo_level,
            CAST(geo_code AS VARCHAR)          AS geo_code,
            CAST(geo_name AS VARCHAR)          AS geo_name,
            CAST(year AS INTEGER)              AS year,
            CAST(population AS BIGINT)         AS population,
            CAST(cohort AS VARCHAR)            AS cohort,
            CAST(measure_code AS VARCHAR)      AS measure_code,
            CAST(measure_label AS VARCHAR)     AS measure_label,
            CAST(short_label AS VARCHAR)       AS short_label,
            CAST(cohort_web_label AS VARCHAR)  AS cohort_web_label,
            CAST(race AS VARCHAR)              AS race,
            CAST(gender AS VARCHAR)            AS gender,
            CAST(observed AS DOUBLE)           AS observed,
            CAST(crude_rate AS DOUBLE)         AS crude_rate,
            CAST(adjusted_rate AS DOUBLE)      AS adjusted_rate,
            CAST(expected AS DOUBLE)           AS expected,
            CAST(expected_adjusted AS DOUBLE)  AS expected_adjusted,
            CAST(oe_ratio AS DOUBLE)           AS oe_ratio,
            CAST(oe_adjusted_ratio AS DOUBLE)  AS oe_adjusted_ratio,
            CAST(std_error AS DOUBLE)          AS std_error,
            CAST(std_error_adjusted AS DOUBLE) AS std_error_adjusted,
            CAST(ci_upper AS DOUBLE)           AS ci_upper,
            CAST(ci_lower AS DOUBLE)           AS ci_lower,
            CAST(percentile AS DOUBLE)         AS percentile
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
    SqlNodeSpec(id=f"{_spec_id(e)}-transform", deps=[_spec_id(e)], sql=_topic_sql(_spec_id(e)))
    for e in TOPIC_ENTITIES
] + [
    SqlNodeSpec(
        id=f"{_spec_id('geography-crosswalk')}-transform",
        deps=[_spec_id("geography-crosswalk")],
        sql=_CROSSWALK_SQL.format(dep=_spec_id("geography-crosswalk")),
    ),
]
