"""Global Entrepreneurship Monitor (GEM) — national-level survey data.

Two published subsets, one per GEM survey instrument:
  - aps-national : Adult Population Survey headline indicators (TEA, perceived
                   opportunities/capabilities, fear of failure, entrepreneurial
                   intentions, established business ownership, ...).
  - nes-national : National Expert Survey — Entrepreneurial Framework Conditions
                   (financing, government policy/programs, education, R&D
                   transfer, market dynamics, cultural/social norms, ...).

Mechanism (research-chosen `bulk_sav`): two static catalog pages list one file
per survey-year. Each file is a ZIP wrapping a single SPSS .sav. DuckDB cannot
read .sav, so the download fn parses each .sav (pyreadstat), reshapes the wide
economy-by-indicator matrix into a tidy long format
(year, economy, indicator, value), and writes one parquet per survey. The SQL
transform is then a thin type-and-filter pass.

The corpus is small (~44 files, a few MB total) and revisions land as updated
fileIds, so this is a stateless full re-pull every refresh — no watermark.

CRITICAL UA QUIRK: the site returns 403 to default Python user agents; we send a
browser User-Agent via configure_http() inside the fetch fn.
"""

import io
import re
import zipfile
import tempfile
import os

import pandas as pd
import pyarrow as pa
import pyreadstat

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    configure_http,
    transient_retry,
    save_raw_parquet,
)

BASE = "https://www.gemconsortium.org"
# A normal browser UA — the site 403s default Python/httpx UAs (ASCII only).
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

# Catalog rows for these supplementary / non-national granularities are dropped
# so we keep exactly one aggregated National Level file per survey-year.
EXCLUDE_TITLE = ("region", "additional", "education", "training", "financing", "individual")

# Pseudo-economies (global aggregate / averages) that appear as a row in some files.
AGGREGATE_NAMES = {"GEM", "GLOBAL", "WORLD", "AVERAGE", "MEAN", "TOTAL", "GLOBAL AVERAGE", "ALL"}

# Identifier / classification columns — never an indicator. Matched on column
# name OR its .sav label (case-insensitive substring).
_ID_LABEL_KW = (
    "country", "region", "income", "classif", "oecd", "brics", "world", "sample",
    "case identif", "phone code", "numeric code", "alpha", "internet", "2-char",
    "2-letter", "2 letter", "pais", "país", "participating", "name",
    "report_income", "country (1)", "worldregion", "identificator", "gcr",
    "original order", "number of expert",
)
_ID_NAME_KW = (
    "country", "ctry", "region", "income", "oecd", "brics", "wbinc", "wefinc",
    "wb_inc", "wb_income", "sample", "worldreg", "classif", "cou_or_reg",
    "report_income", "pais", "país", "crname", "ctryalp", "plotmark",
    "composite_i", "cat_gcr",
)

RAW_SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("economy_code", pa.int64()),
    ("economy_name", pa.string()),
    ("economy_iso", pa.string()),
    ("indicator", pa.string()),
    ("variable", pa.string()),
    ("label", pa.string()),
    ("value", pa.float64()),
])


@transient_retry()
def _fetch_catalog(survey: str) -> str:
    resp = get(f"{BASE}/data/sets", params={"id": survey}, timeout=(10.0, 60.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _fetch_zip(file_id: int) -> bytes:
    resp = get(f"{BASE}/file/open", params={"fileId": file_id}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _select_files(survey: str) -> list[tuple[int, int]]:
    """Scrape a survey catalog page and return [(year, file_id)] — exactly one
    aggregated National Level Data file per survey-year, discovered from source."""
    html = _fetch_catalog(survey)
    chosen: dict[int, tuple] = {}
    for m in re.finditer(r'<tr>\s*<td>(.*?)</td>.*?file="(\d+)"', html, re.S):
        title = re.sub(r"\s+", " ", m.group(1)).strip()
        file_id = int(m.group(2))
        tl = title.lower()
        if "national level data" not in tl:
            continue
        if any(k in tl for k in EXCLUDE_TITLE):
            continue
        ym = re.search(r"gem\s+(\d{4})", tl)
        if not ym:
            continue
        year = int(ym.group(1))
        # Prefer the "Global" titled file, then the highest fileId (latest revision).
        rank = ("global" in tl, file_id)
        if year not in chosen or rank > chosen[year][0]:
            chosen[year] = (rank, file_id)
    if not chosen:
        raise AssertionError(f"{survey}: no National Level Data files found on catalog page")
    return sorted((year, v[1]) for year, v in chosen.items())


def _is_id_col(col: str, label: str) -> bool:
    nl = col.lower()
    ll = (label or "").lower()
    return any(k in ll for k in _ID_LABEL_KW) or any(k in nl for k in _ID_NAME_KW)


def _is_junk_col(col: str) -> bool:
    """Dispersion stats, non-standard scale variants and z-scores are not
    headline measures — drop them to keep the long table interpretable."""
    nl = col.lower()
    if nl in ("id", "eu", "oecd", "brics", "region", "worldregion", "means", "means_10", "col"):
        return True
    if re.search(r"(sd|std|stde|_se|med)\d*$", nl):
        return True
    if re.search(r"mean[5-9]$", nl):
        return True
    if nl.startswith("z"):
        return True
    return False


def _pick_code_col(df: pd.DataFrame, labels: dict) -> str | None:
    for c in df.columns:
        if not pd.api.types.is_numeric_dtype(df[c]):
            continue
        nl = c.lower()
        ll = (labels.get(c) or "").lower()
        if ("country" in nl or "ctry" in nl or "crcode" in nl) and (
            "numeric" in ll or "phone" in ll or "code" in ll or "country" in ll
        ):
            return c
    return None


def _pick_name_col(df: pd.DataFrame, labels: dict) -> str | None:
    """The string column carrying full economy names (longest mean length wins)."""
    best, best_score = None, (0.0, 0.0)
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            continue
        ll = (labels.get(c) or "").lower()
        if "2" in ll and any(k in ll for k in ("letter", "char", "internet", "alpha")):
            continue  # that's the ISO code column, not the name
        vals = df[c].dropna().astype(str)
        if vals.empty:
            continue
        mean_len = float(vals.str.len().mean())
        if mean_len < 3:
            continue
        bonus = 1.0 if "name" in ll else 0.0
        score = (bonus, mean_len)
        if score > best_score:
            best_score, best = score, c
    return best


def _pick_iso_col(df: pd.DataFrame, labels: dict) -> str | None:
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            continue
        ll = (labels.get(c) or "").lower()
        if "2" in ll and any(k in ll for k in ("letter", "char", "alpha", "internet")):
            return c
    return None


def _reshape(df: pd.DataFrame, meta, year: int, survey: str) -> pd.DataFrame:
    """Wide economy-by-indicator .sav frame -> tidy long rows."""
    labels = meta.column_names_to_labels
    code_col = _pick_code_col(df, labels)
    name_col = _pick_name_col(df, labels)
    iso_col = _pick_iso_col(df, labels)
    value_labels = meta.variable_value_labels.get(code_col, {}) if code_col else {}

    value_cols = [
        c for c in df.columns
        if pd.api.types.is_numeric_dtype(df[c])
        and c != code_col
        and not _is_id_col(c, labels.get(c))
        and not _is_junk_col(c)
    ]
    if not value_cols:
        raise AssertionError(f"{survey} {year}: no indicator columns identified")

    base = pd.DataFrame(index=df.index)
    base["economy_code"] = df[code_col] if code_col else pd.NA
    # economy name: prefer the code's value-labels (present even when no name
    # column exists, e.g. recent NES files), else a string name column.
    name_from_labels = df[code_col].map(value_labels) if (code_col and value_labels) else None
    name_from_col = df[name_col] if name_col else None
    if name_from_labels is not None and name_from_col is not None:
        base["economy_name"] = name_from_labels.where(name_from_labels.notna(), name_from_col)
    elif name_from_labels is not None:
        base["economy_name"] = name_from_labels
    elif name_from_col is not None:
        base["economy_name"] = name_from_col
    else:
        base["economy_name"] = pd.NA
    base["economy_iso"] = df[iso_col] if iso_col else pd.NA

    wide = pd.concat([base, df[value_cols]], axis=1)
    long = wide.melt(
        id_vars=["economy_code", "economy_name", "economy_iso"],
        value_vars=value_cols,
        var_name="variable",
        value_name="value",
    )
    long = long.dropna(subset=["value"])

    long["year"] = year
    long["label"] = long["variable"].map(labels)
    long["indicator"] = long["variable"]
    if survey == "aps":
        # APS columns embed the 2-digit survey year (TEA22, Opport22); strip it
        # so an indicator joins across years into one series.
        yy = f"{year % 100:02d}"
        mask = (long["variable"].str.len() > 2) & (long["variable"].str.lower().str[-2:] == yy)
        long.loc[mask, "indicator"] = long.loc[mask, "variable"].str[:-2]

    # Drop global-aggregate pseudo-economy rows.
    name_upper = long["economy_name"].astype("string").str.strip().str.upper()
    keep = ~name_upper.isin(AGGREGATE_NAMES)
    keep &= ~(long["economy_code"].fillna(-1) == 0)
    long = long[keep]

    return long[["year", "economy_code", "economy_name", "economy_iso",
                 "indicator", "variable", "label", "value"]]


def _read_sav_from_zip(content: bytes) -> tuple[pd.DataFrame, object]:
    zf = zipfile.ZipFile(io.BytesIO(content))
    names = [n for n in zf.namelist() if n.lower().endswith(".sav") and not n.startswith("__MACOSX")]
    if not names:
        raise AssertionError(f"zip has no .sav member: {zf.namelist()}")
    data = zf.read(names[0])
    # pyreadstat reads from a path; the .sav is small (<1MB), so a temp file is fine.
    tmp = tempfile.NamedTemporaryFile(suffix=".sav", delete=False)
    try:
        tmp.write(data)
        tmp.close()
        return pyreadstat.read_sav(tmp.name)
    finally:
        os.unlink(tmp.name)


def fetch_one(node_id: str) -> None:
    """Fetch + reshape all National Level Data files for one survey into one
    long-format parquet. node_id is e.g. 'gem-entrepreneurship-aps-national'."""
    configure_http(headers={"User-Agent": BROWSER_UA})
    entity = node_id[len("gem-entrepreneurship-"):]   # 'aps-national' / 'nes-national'
    survey = entity.split("-")[0]                       # 'aps' / 'nes'

    frames: list[pd.DataFrame] = []
    for year, file_id in _select_files(survey):
        df, meta = _read_sav_from_zip(_fetch_zip(file_id))
        frames.append(_reshape(df, meta, year, survey))

    combined = pd.concat(frames, ignore_index=True)
    combined["economy_code"] = pd.to_numeric(combined["economy_code"], errors="coerce").astype("Int64")
    for col in ("economy_name", "economy_iso", "indicator", "variable", "label"):
        combined[col] = combined[col].astype("string")
    combined["value"] = pd.to_numeric(combined["value"], errors="coerce")
    combined = combined.dropna(subset=["value", "indicator"])

    table = pa.Table.from_pandas(combined, schema=RAW_SCHEMA, preserve_index=False)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="gem-entrepreneurship-aps-national", fn=fetch_one, kind="download"),
    NodeSpec(id="gem-entrepreneurship-nes-national", fn=fetch_one, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=f'''
            SELECT
                CAST(year AS INTEGER)      AS year,
                economy_code,
                economy_name,
                economy_iso,
                indicator,
                variable,
                label,
                CAST(value AS DOUBLE)      AS value
            FROM "{spec.id}"
            WHERE value IS NOT NULL
              AND indicator IS NOT NULL
        ''',
    )
    for spec in DOWNLOAD_SPECS
]
