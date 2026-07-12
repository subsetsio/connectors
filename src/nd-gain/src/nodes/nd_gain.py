"""ND-GAIN Country Index connector.

The Notre Dame Global Adaptation Initiative publishes the entire Country Index as
one bulk ZIP of wide-format CSVs (columns ISO3, Name, then one column per year).
There is no catalog or queryable API, so each download node:

  1. GETs the download page (static HTML) and scrapes the single timestamped ZIP
     href (the filename changes every annual release, so it is never hardcoded),
  2. downloads the ZIP (~4.6 MB, the whole corpus),
  3. reshapes the wide CSVs it owns into long format,
  4. saves one parquet raw asset.

Stateless full re-pull: the corpus is tiny and updates ~annually, so every run
re-fetches everything and overwrites. No watermark, no incremental query (the
source exposes none). Freshness gating is the maintain step's job.

Five subsets, one download + one transform each:
  gain          - overall ND-GAIN index score per country-year
  vulnerability - vulnerability overall + 6 sectors + 3 components (long, category col)
  readiness     - readiness overall + 3 sectors (long, category col)
  indicators    - 45 underlying indicators + context (gdp/pop/hdi); raw/input/score values
  trends        - per-country historical trend slope + sign for the 3 headline measures
"""

import io
import re
import zipfile

import httpx
import pandas as pd
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
)
import subsets_utils.http_client as http_client

DOWNLOAD_PAGE = "https://gain-new.crc.nd.edu/about/download"
HOST = "https://gain-new.crc.nd.edu"
ZIP_HREF_RE = re.compile(r'href="(/assets/gain/files/resources-[^"]+\.zip)"')
YEAR_RE = re.compile(r"^\d{4}$")

_HTTP_READY = False


def _ensure_http() -> None:
    """Use a verify-disabled client for ND-GAIN's public file host.

    GitHub Actions cannot build a valid chain for gain-new.crc.nd.edu, while
    the same public ZIP is otherwise accessible. Keep requests flowing through
    subsets_utils.get so retry and request logging still work.
    """
    global _HTTP_READY
    if _HTTP_READY:
        return
    if http_client._client is not None:
        http_client._client.close()
    http_client._client = httpx.Client(
        timeout=httpx.Timeout(180.0),
        headers={"User-Agent": "subsets-nd-gain/1.0"},
        follow_redirects=True,
        verify=False,
    )
    _HTTP_READY = True


def _http_get(url: str):
    _ensure_http()
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp


def _load_zip() -> zipfile.ZipFile:
    """Scrape the download page for the current ZIP link and return it opened."""
    html = _http_get(DOWNLOAD_PAGE).text
    hrefs = ZIP_HREF_RE.findall(html)
    if not hrefs:
        raise RuntimeError(
            f"no resources-*.zip href found on {DOWNLOAD_PAGE} - page layout changed"
        )
    content = _http_get(HOST + hrefs[0]).content
    return zipfile.ZipFile(io.BytesIO(content))


def _read_csv(zf: zipfile.ZipFile, path: str) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(zf.read(path)))


def _melt_years(df: pd.DataFrame, value_name: str) -> pd.DataFrame:
    """Wide (ISO3, Name, <year cols>) -> long (iso3, country, year, <value_name>)."""
    year_cols = [c for c in df.columns if YEAR_RE.match(str(c))]
    if not year_cols:
        raise RuntimeError(f"no year columns found; got {list(df.columns)[:6]}")
    long = df.melt(
        id_vars=["ISO3", "Name"],
        value_vars=year_cols,
        var_name="year",
        value_name=value_name,
    )
    long["year"] = long["year"].astype(int)
    return long.rename(columns={"ISO3": "iso3", "Name": "country"})


def _to_parquet(df: pd.DataFrame, schema: pa.Schema, asset: str) -> None:
    table = pa.Table.from_pandas(df[schema.names], preserve_index=False).cast(schema)
    save_raw_parquet(table, asset)


# --- schemas (the contract for each raw asset) ------------------------------

SCORE_SCHEMA = pa.schema([
    ("iso3", pa.string()),
    ("country", pa.string()),
    ("year", pa.int32()),
    ("score", pa.float64()),
])

CATEGORY_SCHEMA = pa.schema([
    ("iso3", pa.string()),
    ("country", pa.string()),
    ("year", pa.int32()),
    ("category", pa.string()),
    ("score", pa.float64()),
])

INDICATOR_SCHEMA = pa.schema([
    ("iso3", pa.string()),
    ("country", pa.string()),
    ("year", pa.int32()),
    ("indicator_id", pa.string()),
    ("raw_value", pa.float64()),
    ("input_value", pa.float64()),
    ("score_value", pa.float64()),
])

TREND_SCHEMA = pa.schema([
    ("iso3", pa.string()),
    ("country", pa.string()),
    ("measure", pa.string()),
    ("value", pa.float64()),
    ("sign", pa.int32()),
])


# --- fetch functions --------------------------------------------------------

def fetch_gain(node_id: str) -> None:
    zf = _load_zip()
    long = _melt_years(_read_csv(zf, "resources/gain/gain.csv"), "score")
    long = long.dropna(subset=["score"])
    _to_parquet(long, SCORE_SCHEMA, node_id)


def _fetch_grouped(node_id: str, group: str) -> None:
    """Melt every non-delta CSV under resources/<group>/, tagging each with its
    category (the file stem; the overall index file shares the group's name)."""
    zf = _load_zip()
    prefix = f"resources/{group}/"
    paths = sorted(
        n for n in zf.namelist()
        if n.startswith(prefix) and n.endswith(".csv") and not n.endswith("_delta.csv")
    )
    if not paths:
        raise RuntimeError(f"no CSVs under {prefix} - ZIP layout changed")
    frames = []
    for path in paths:
        category = path[len(prefix):-len(".csv")]
        long = _melt_years(_read_csv(zf, path), "score")
        long["category"] = category
        frames.append(long)
    out = pd.concat(frames, ignore_index=True).dropna(subset=["score"])
    _to_parquet(out, CATEGORY_SCHEMA, node_id)


def fetch_vulnerability(node_id: str) -> None:
    _fetch_grouped(node_id, "vulnerability")


def fetch_readiness(node_id: str) -> None:
    _fetch_grouped(node_id, "readiness")


def fetch_indicators(node_id: str) -> None:
    """For every indicator folder, join its raw/input/score variants on
    (iso3, country, year) into one long row carrying all three values."""
    zf = _load_zip()
    names = set(zf.namelist())
    ind_dirs = sorted({
        n.split("/")[2]
        for n in names
        if n.startswith("resources/indicators/") and len(n.split("/")) > 3
    })
    if not ind_dirs:
        raise RuntimeError("no indicator folders found - ZIP layout changed")
    variants = [("raw_value", "raw.csv"), ("input_value", "input.csv"), ("score_value", "score.csv")]
    frames = []
    for ind in ind_dirs:
        merged = None
        for value_name, fname in variants:
            path = f"resources/indicators/{ind}/{fname}"
            if path not in names:
                continue
            part = _melt_years(_read_csv(zf, path), value_name)
            merged = part if merged is None else merged.merge(
                part, on=["iso3", "country", "year"], how="outer"
            )
        if merged is None:
            continue
        for value_name, _ in variants:
            if value_name not in merged.columns:
                merged[value_name] = pd.NA
        merged["indicator_id"] = ind
        frames.append(merged)
    out = pd.concat(frames, ignore_index=True)
    value_cols = ["raw_value", "input_value", "score_value"]
    out = out.dropna(subset=value_cols, how="all")
    _to_parquet(out, INDICATOR_SCHEMA, node_id)


def fetch_trends(node_id: str) -> None:
    """resources/trends/<measure>.csv: one row per country, columns ISO3, Name,
    Value, sign. Stack the three measures into one long table."""
    zf = _load_zip()
    prefix = "resources/trends/"
    paths = sorted(n for n in zf.namelist() if n.startswith(prefix) and n.endswith(".csv"))
    if not paths:
        raise RuntimeError("no trend CSVs found - ZIP layout changed")
    frames = []
    for path in paths:
        measure = path[len(prefix):-len(".csv")]
        df = _read_csv(zf, path).rename(
            columns={"ISO3": "iso3", "Name": "country", "Value": "value"}
        )
        df["measure"] = measure
        frames.append(df[["iso3", "country", "measure", "value", "sign"]])
    out = pd.concat(frames, ignore_index=True).dropna(subset=["value"])
    out["sign"] = out["sign"].astype("int64")
    _to_parquet(out, TREND_SCHEMA, node_id)


# --- specs ------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="nd-gain-gain", fn=fetch_gain, kind="download"),
    NodeSpec(id="nd-gain-vulnerability", fn=fetch_vulnerability, kind="download"),
    NodeSpec(id="nd-gain-readiness", fn=fetch_readiness, kind="download"),
    NodeSpec(id="nd-gain-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="nd-gain-trends", fn=fetch_trends, kind="download"),
]
