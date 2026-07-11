"""Open Source Asset Pricing (Chen & Zimmermann) connector.

Source: https://www.openassetpricing.com/ — cross-sectional stock-return
predictor portfolios and signal documentation, published as CSV/zip files in a
public Google Drive folder, one folder per annual release.

Strategy (stateless full re-pull): each refresh, discover the current release
root folder (scraped from the data page, with a pinned fallback), walk it to map
file-name -> Drive file-id, download the file(s) for each subset via the public
`uc?export=download` endpoint, and overwrite. File ids change every release, so
they are resolved at fetch time, never hardcoded. No incremental query exists
(annual full release); all three files are small (<60MB) so a full re-pull is
cheap. The 1.6GB firm-level microdata panel is intentionally not built (ranked
below the publish threshold — firm-month microdata, not aggregate time series).
"""

import csv
import io
import itertools
import json
import re

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    save_raw_ndjson,
)

# Pinned fallback: Oct-2025 (v2.0.0) release root folder. Discovery scrapes the
# data page first so new releases are picked up automatically; this is only used
# if that scrape fails.
FALLBACK_RELEASE_FOLDER = "1qQDuTsnyvWfEJR6nPBQZ8xxlq6bkLG_y"
DATA_PAGE = "https://www.openassetpricing.com/data/"

# Per-predictor / per-stock subfolders hold hundreds of split files we never
# resolve by name; skip them while walking to keep the listing cheap.
_SKIP_FOLDERS = {"Individual", "Predictors"}
_FOLDER_MIME = "application/vnd.google-apps.folder"


@transient_retry()
def _drive_html(url):
    r = get(url, timeout=(10.0, 90.0))
    r.raise_for_status()
    return r.text


def _list_folder(folder_id):
    """Return [(file_id, name, mime), ...] for one Drive folder via its public
    web listing (the `_DRIVE_ivd` embedded array). No auth required."""
    html = _drive_html(f"https://drive.google.com/drive/folders/{folder_id}?hl=en")
    m = re.search(r"_DRIVE_ivd'\]\s*=\s*'((?:[^'\\]|\\.)*)'", html)
    if not m:
        raise RuntimeError(f"could not locate _DRIVE_ivd in folder listing {folder_id}")
    decoded = m.group(1).encode("utf-8").decode("unicode_escape")
    arr = json.loads(decoded)
    items = arr[0] or []
    return [(e[0], e[2], e[3]) for e in items]


def _resolve_release_root():
    """Discover the current release root folder id from the data page (the
    folder that contains SignalDoc.csv at top level); fall back to the pin."""
    try:
        html = _drive_html(DATA_PAGE)
        seen = []
        for fid in re.findall(r"/drive/folders/([-\w]{20,})", html):
            if fid not in seen:
                seen.append(fid)
        for fid in seen:
            try:
                names = {name for _, name, _ in _list_folder(fid)}
            except Exception:
                continue
            if "SignalDoc.csv" in names:
                return fid
    except Exception as exc:  # discovery is best-effort; pin is the safety net
        print(f"release discovery failed ({type(exc).__name__}: {exc}); using fallback")
    return FALLBACK_RELEASE_FOLDER


def _name_to_id(root_id):
    """Recursively walk the release folder and return {file_name: file_id}.
    First occurrence wins; the target file names are unique across the tree."""
    mapping = {}
    stack = [root_id]
    while stack:
        fid = stack.pop()
        for child_id, name, mime in _list_folder(fid):
            if mime == _FOLDER_MIME:
                if name not in _SKIP_FOLDERS:
                    stack.append(child_id)
            else:
                mapping.setdefault(name, child_id)
    return mapping


@transient_retry()
def _download_csv_text(file_id):
    """Download a public Drive file via the uc endpoint and return its text.
    Handles Google's large-file virus-scan interstitial defensively (the three
    files this connector pulls are small enough to download directly)."""
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    r = get(url, timeout=(10.0, 300.0))
    r.raise_for_status()
    ct = r.headers.get("content-type", "")
    if ct.startswith("text/html"):
        # Virus-scan confirmation page: follow the download-form action.
        m = re.search(r'action="(https://[^"]*?download[^"]*)"', r.text)
        if not m:
            raise RuntimeError(f"unexpected HTML response for file {file_id}")
        action = m.group(1).replace("&amp;", "&")
        params = dict(re.findall(r'name="([^"]+)"\s+value="([^"]*)"', r.text))
        r = get(action, params=params, timeout=(10.0, 300.0))
        r.raise_for_status()
    return r.content.decode("utf-8", "replace")


def _resolve_file(file_name):
    root = _resolve_release_root()
    mapping = _name_to_id(root)
    if file_name not in mapping:
        raise RuntimeError(
            f"{file_name!r} not found in release folder {root}; "
            f"available top names sample: {sorted(mapping)[:15]}"
        )
    return mapping[file_name]


def _to_float(v):
    v = (v or "").strip()
    if v in ("", "NA", "NaN", "nan", "."):
        return None
    return float(v)


def _to_int(v):
    f = _to_float(v)
    return int(f) if f is not None else None


# ---------------------------------------------------------------------------
# Fetch functions — one per subset (entity). Each writes its own raw asset.
# ---------------------------------------------------------------------------

def fetch_predictor_docs(node_id: str) -> None:
    """SignalDoc.csv — the predictor codebook (free-text heavy, mixed types).
    Saved as ndjson (all values as strings); the transform re-types."""
    asset = node_id
    text = _download_csv_text(_resolve_file("SignalDoc.csv"))
    reader = csv.DictReader(io.StringIO(text))
    rows = [{(k or "").strip(): (v if v != "" else None) for k, v in r.items()}
            for r in reader]
    if not rows:
        raise RuntimeError("SignalDoc.csv parsed to 0 rows")
    save_raw_ndjson(rows, asset)


_LS_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("predictor", pa.string()),
    ("ret", pa.float64()),
])


def fetch_long_short_returns(node_id: str) -> None:
    """PredictorLSretWide.csv — wide monthly long-short returns (date + one
    column per predictor). Melted to long (date, predictor, ret); 'NA' cells
    dropped."""
    asset = node_id
    text = _download_csv_text(_resolve_file("PredictorLSretWide.csv"))
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    if not header or header[0] != "date":
        raise RuntimeError(f"unexpected PredictorLSretWide header: {header[:5]}")
    predictors = header[1:]
    dates, preds, rets = [], [], []
    for row in reader:
        if not row:
            continue
        d = row[0]
        for j, cell in enumerate(row[1:]):
            val = _to_float(cell)
            if val is None:
                continue
            dates.append(d)
            preds.append(predictors[j])
            rets.append(val)
    if not dates:
        raise RuntimeError("PredictorLSretWide melted to 0 rows")
    table = pa.table({"date": dates, "predictor": preds, "ret": rets}, schema=_LS_SCHEMA)
    save_raw_parquet(table, asset)


_PORT_SCHEMA = pa.schema([
    ("signalname", pa.string()),
    ("port", pa.string()),
    ("date", pa.string()),
    ("ret", pa.float64()),
    ("signallag", pa.float64()),
    ("Nlong", pa.int64()),
    ("Nshort", pa.int64()),
])


def fetch_portfolio_sorts(node_id: str) -> None:
    """PredictorPortsFull.csv — long-format decile (01-10) + long-short (LS)
    portfolio returns per predictor, original-paper methodology."""
    asset = node_id
    text = _download_csv_text(_resolve_file("PredictorPortsFull.csv"))
    reader = csv.DictReader(io.StringIO(text))
    expected = {"signalname", "port", "date", "ret", "signallag", "Nlong", "Nshort"}
    missing = expected - set(reader.fieldnames or [])
    if missing:
        raise RuntimeError(f"PredictorPortsFull missing columns: {missing}")
    signalname, port, date, ret, signallag, nlong, nshort = [], [], [], [], [], [], []
    for r in reader:
        signalname.append(r["signalname"])
        port.append(r["port"])
        date.append(r["date"])
        ret.append(_to_float(r["ret"]))
        signallag.append(_to_float(r["signallag"]))
        nlong.append(_to_int(r["Nlong"]))
        nshort.append(_to_int(r["Nshort"]))
    if not date:
        raise RuntimeError("PredictorPortsFull parsed to 0 rows")
    table = pa.table({
        "signalname": signalname, "port": port, "date": date, "ret": ret,
        "signallag": signallag, "Nlong": nlong, "Nshort": nshort,
    }, schema=_PORT_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="open-source-asset-pricing-predictor-docs",
             fn=fetch_predictor_docs, kind="download"),
    NodeSpec(id="open-source-asset-pricing-long-short-returns",
             fn=fetch_long_short_returns, kind="download"),
    NodeSpec(id="open-source-asset-pricing-portfolio-sorts",
             fn=fetch_portfolio_sorts, kind="download"),
]
