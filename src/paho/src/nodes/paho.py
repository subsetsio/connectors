"""Download specs for PAHO Core Indicators."""

from __future__ import annotations

import io
import re
import zipfile
from datetime import datetime, timezone
from types import SimpleNamespace
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pandas as pd
import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    load_state,
    raw_asset_exists,
    record_source_signature,
    save_state,
    save_raw_parquet,
)


SLUG = "paho"
DOWNLOAD_PAGE_URL = "https://opendata.paho.org/en/core-indicators/download-dataset"
FALLBACK_ZIP_URL = "https://opendata.paho.org/sites/default/files/data/2026-04/paho-core-indicators-2026-20260413.zip"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; subsets.io data connector; https://subsets.io)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
ZIP_HEADERS = {
    **REQUEST_HEADERS,
    "Accept": "application/zip,*/*;q=0.8",
    "Referer": DOWNLOAD_PAGE_URL,
}
SOURCE_SIGNATURES_KEY = "source_signatures"

VALUE_COLUMNS = [
    "paho_indicator_id",
    "indicator_name",
    "nombre_indicador",
    "spatial_dim_type",
    "spatial_dim",
    "spatial_dim_en",
    "spatial_dim_es",
    "time_dim_type",
    "time_dim",
    "numeric_value",
    "value_as_string",
    "low",
    "high",
    "technical_note",
    "nota_tecnica",
    "data_source_type",
    "data_source_specific",
    "data_provider_type",
    "data_provider_specific",
    "data_secondary_source",
    "type_statistics",
    "public_private",
    "public_private_sp",
    "source_url",
    "preliminary",
    "published_at",
    "accessed_at",
]

VALUE_SCHEMA = pa.schema(
    [
        ("paho_indicator_id", pa.int64()),
        ("indicator_name", pa.string()),
        ("nombre_indicador", pa.string()),
        ("spatial_dim_type", pa.string()),
        ("spatial_dim", pa.string()),
        ("spatial_dim_en", pa.string()),
        ("spatial_dim_es", pa.string()),
        ("time_dim_type", pa.string()),
        ("time_dim", pa.string()),
        ("numeric_value", pa.float64()),
        ("value_as_string", pa.string()),
        ("low", pa.float64()),
        ("high", pa.float64()),
        ("technical_note", pa.string()),
        ("nota_tecnica", pa.string()),
        ("data_source_type", pa.string()),
        ("data_source_specific", pa.string()),
        ("data_provider_type", pa.string()),
        ("data_provider_specific", pa.string()),
        ("data_secondary_source", pa.string()),
        ("type_statistics", pa.string()),
        ("public_private", pa.string()),
        ("public_private_sp", pa.string()),
        ("source_url", pa.string()),
        ("preliminary", pa.string()),
        ("published_at", pa.string()),
        ("accessed_at", pa.string()),
    ]
)

INDICATOR_SCHEMA = pa.schema(
    [
        ("paho_indicator_id", pa.int64()),
        ("indicator_name", pa.string()),
        ("nombre_indicador", pa.string()),
    ]
)


def _latest_zip_url(page_html: str) -> str:
    match = re.search(r'https://opendata\.paho\.org/sites/default/files/data/[^"\']+\.zip', page_html)
    if not match:
        raise RuntimeError("PAHO download page did not expose a Core Indicators ZIP link")
    return match.group(0)


def _fetch_url(url: str, headers: dict[str, str], *, timeout: float = 180.0) -> tuple[bytes, object]:
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=timeout) as resp:
            content = resp.read()
            response = SimpleNamespace(headers=resp.headers, url=resp.geturl(), status_code=resp.status)
            return content, response
    except HTTPError as exc:
        raise RuntimeError(f"PAHO request failed with HTTP {exc.code} for {url}") from exc


def _head_headers(url: str, headers: dict[str, str], *, timeout: float = 30.0):
    req = Request(url, headers=headers, method="HEAD")
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.headers
    except Exception:
        return None


def _signature(headers) -> dict[str, str] | None:
    etag = headers.get("ETag")
    last_modified = headers.get("Last-Modified")
    if not etag and not last_modified:
        return None
    sig = {}
    if etag:
        sig["etag"] = etag
    if last_modified:
        sig["last_modified"] = last_modified
    return sig


def _norm_etag(value: str) -> str:
    return value[2:] if value.startswith("W/") else value


def _record_signature_from_response(asset_id: str, url: str, response: object) -> None:
    if record_source_signature(asset_id, url, response=response) is not None:
        return

    sig = _signature(response.headers)
    if sig is None:
        return
    sig["recorded_at"] = datetime.now(timezone.utc).isoformat()
    state = load_state(asset_id)
    sigs = state.get(SOURCE_SIGNATURES_KEY)
    if not isinstance(sigs, dict):
        sigs = {}
    sigs[url] = sig
    state[SOURCE_SIGNATURES_KEY] = sigs
    save_state(asset_id, state)


def _source_unchanged_urllib(asset_id: str, url: str, headers: dict[str, str]) -> bool:
    sigs = load_state(asset_id).get(SOURCE_SIGNATURES_KEY)
    stored = sigs.get(url) if isinstance(sigs, dict) else None
    if not isinstance(stored, dict):
        return False

    current_headers = _head_headers(url, headers)
    if current_headers is None:
        return False
    current = _signature(current_headers)
    if current is None:
        return False

    if stored.get("etag") and current.get("etag"):
        return _norm_etag(stored["etag"]) == _norm_etag(current["etag"])
    if stored.get("last_modified") and current.get("last_modified"):
        return stored["last_modified"] == current["last_modified"]
    return False


def _resolve_zip_url() -> tuple[str, object | None]:
    try:
        page_bytes, page_resp = _fetch_url(DOWNLOAD_PAGE_URL, REQUEST_HEADERS, timeout=60.0)
    except RuntimeError as exc:
        print(f"{exc}; falling back to researched ZIP {FALLBACK_ZIP_URL}")
        return FALLBACK_ZIP_URL, None
    return _latest_zip_url(page_bytes.decode("utf-8", errors="replace")), page_resp


def _download_dataframe() -> tuple[pd.DataFrame, object | None, object]:
    zip_url, page_resp = _resolve_zip_url()

    zip_bytes, zip_resp = _fetch_url(zip_url, ZIP_HEADERS, timeout=180.0)
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        csv_names = [name for name in zf.namelist() if name.lower().endswith(".csv")]
        if len(csv_names) != 1:
            raise RuntimeError(f"expected exactly one CSV in PAHO ZIP, found {csv_names!r}")
        with zf.open(csv_names[0]) as csv_file:
            df = pd.read_csv(csv_file, dtype=str, na_values=["NULL"], keep_default_na=False)

    missing = set(VALUE_COLUMNS) - set(df.columns)
    if missing:
        raise RuntimeError(f"PAHO CSV is missing expected columns: {sorted(missing)}")
    return df[VALUE_COLUMNS], page_resp, zip_resp


def _coerce_values_table(df: pd.DataFrame) -> pa.Table:
    out = df.copy()
    for col in ["paho_indicator_id"]:
        out[col] = pd.to_numeric(out[col], errors="raise")
    for col in ["numeric_value", "low", "high"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return pa.Table.from_pandas(out, schema=VALUE_SCHEMA, preserve_index=False)


def _coerce_indicators_table(df: pd.DataFrame) -> pa.Table:
    indicators = (
        df[["paho_indicator_id", "indicator_name", "nombre_indicador"]]
        .drop_duplicates()
        .sort_values(["paho_indicator_id", "indicator_name"])
        .reset_index(drop=True)
    )
    indicators["paho_indicator_id"] = pd.to_numeric(indicators["paho_indicator_id"], errors="raise")
    return pa.Table.from_pandas(indicators, schema=INDICATOR_SCHEMA, preserve_index=False)


def fetch_core_indicator_values(node_id: str) -> None:
    df, page_resp, zip_resp = _download_dataframe()
    save_raw_parquet(_coerce_values_table(df), node_id)
    if page_resp is not None:
        _record_signature_from_response(node_id, DOWNLOAD_PAGE_URL, page_resp)
    _record_signature_from_response(node_id, str(zip_resp.url), zip_resp)


def fetch_core_indicators(node_id: str) -> None:
    df, page_resp, zip_resp = _download_dataframe()
    save_raw_parquet(_coerce_indicators_table(df), node_id)
    if page_resp is not None:
        _record_signature_from_response(node_id, DOWNLOAD_PAGE_URL, page_resp)
    _record_signature_from_response(node_id, str(zip_resp.url), zip_resp)


def _fresh(aid: str) -> bool:
    return raw_asset_exists(aid, "parquet") and (
        _source_unchanged_urllib(aid, DOWNLOAD_PAGE_URL, REQUEST_HEADERS)
        or _source_unchanged_urllib(aid, FALLBACK_ZIP_URL, ZIP_HEADERS)
    )


DOWNLOAD_SPECS = [
    NodeSpec(id="paho-core-indicator-values", fn=fetch_core_indicator_values, kind="download"),
    NodeSpec(id="paho-core-indicators", fn=fetch_core_indicators, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="paho-core-indicator-values",
        description="Core Indicators download page is checked for Last-Modified/ETag; full data updates are cited on the page.",
        check=_fresh,
    ),
    MaintainSpec(
        asset_id="paho-core-indicators",
        description="Core Indicators download page is checked for Last-Modified/ETag; full data updates are cited on the page.",
        check=_fresh,
    ),
]
