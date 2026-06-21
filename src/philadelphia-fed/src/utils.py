"""Shared helpers for the Federal Reserve Bank of Philadelphia connector.

The Philadelphia Fed publishes each survey/index as bulk Excel/CSV workbook(s) at
stable /-/media/FRBP/Assets/Surveys-And-Data/ URLs. There is no API: each entity is
one (or a few) downloadable files with a bespoke layout, parsed into clean
long-format parquet by the per-subset node modules. This module holds only the code
shared across those modules: base URLs, the HTTP fetchers with transient retry, the
SAS-malformed-xlsx sanitizer, and the common write/date helpers. No NodeSpecs live
here, so the node loader (which scans nodes/ for *_SPECS) never picks it up.

Quirk handled globally: the SPF/dispersion/RTDSM workbooks are written by SAS, which
emits a malformed W3CDTF timestamp in docProps/core.xml ('2026-05-13T 2:56:52' — a
space where the zero-padded hour should be). openpyxl refuses to parse it, so
`_read_xlsx` rebuilds the zip with a clean core.xml before handing bytes to pandas.
"""

import io
import zipfile

import httpx
import pyarrow as pa
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import get, save_raw_parquet

# NOTE: `pandas` is imported lazily inside each function rather than at module
# level. The harness's spec-introspection subprocess (_spec_dump.py) runs from
# the repo's hardened/ dir, which shadows the stdlib `secrets` module that
# numpy.random imports on init — a module-level `import pandas` would crash
# introspection. The production run (via src/main.py) is unaffected; the lazy
# import is only to keep this module importable under that introspection path.

MEDIA = "https://www.philadelphiafed.org/-/media/FRBP/Assets"
SND = f"{MEDIA}/Surveys-And-Data"

# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
_TRANSIENT = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError, httpx.ProxyError,
)


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _TRANSIENT):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    ct = resp.headers.get("content-type", "")
    # The site soft-404s by serving an 18KB HTML page with HTTP 200 for a bad path.
    if "text/html" in ct:
        raise AssertionError(f"expected a data file but got HTML (soft-404) from {url}")
    return resp.content


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _fetch_html(url: str) -> str:
    """Fetch an HTML page (the RTDSM file index) — no soft-404 content-type guard."""
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


# ---------------------------------------------------------------------------
# Excel helpers
# ---------------------------------------------------------------------------
_CLEAN_CORE = (
    b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    b'<cp:coreProperties '
    b'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    b'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
    b'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
    b'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"></cp:coreProperties>'
)


def _read_xlsx(content: bytes) -> "pd.ExcelFile":
    """Return a pandas ExcelFile for an .xlsx, sanitizing the SAS-malformed
    docProps/core.xml that otherwise makes openpyxl raise on the document date."""
    import pandas as pd
    src = zipfile.ZipFile(io.BytesIO(content))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = _CLEAN_CORE if item.filename == "docProps/core.xml" else src.read(item.filename)
            dst.writestr(item, data)
    return pd.ExcelFile(io.BytesIO(out.getvalue()), engine="openpyxl")


def _write(rows: list[dict], schema: pa.Schema, asset: str) -> None:
    if not rows:
        raise AssertionError(f"{asset}: parsed 0 rows")
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, asset)


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------
def _ymd(val) -> str | None:
    """A pandas/py datetime -> 'YYYY-MM-DD'."""
    import pandas as pd
    if pd.isna(val):
        return None
    ts = pd.Timestamp(val)
    return ts.strftime("%Y-%m-%d")
