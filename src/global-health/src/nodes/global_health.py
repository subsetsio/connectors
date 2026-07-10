"""Global.health outbreak line-lists and variant timeseries.

One download node per accepted collect entity. Each entity is a single CSV
fetched in full every run (stateless full re-pull — the files are small and
these are concluded/static outbreaks, so there is no incremental filter and no
watermark). The CSV is parsed to line-delimited JSON with empty cells mapped to
null; column types are left to the model stage (line lists carry banded ages,
free text and messy dates, so string-typed raw is the honest, drift-safe shape).

Fetch surface per entity is data, declared in src/constants.py: committed CSVs
come from raw.githubusercontent.com on the default branch; actively-curated
outbreaks come from the repo's AWS API-Gateway latest.csv. See constants.py.
"""
import csv
import io
from urllib.parse import quote

from subsets_utils import NodeSpec, get, save_raw_ndjson, transient_retry

from constants import ENTITY_CONFIG

SLUG = "global-health"


@transient_retry()
def _fetch(url, params=None):
    resp = get(url, params=params, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp


def _sanitize_header(hdr):
    """Trim header names; fill blanks/duplicates with positional names."""
    seen = {}
    out = []
    for i, raw in enumerate(hdr):
        name = (raw or "").strip()
        if not name:
            name = f"col_{i + 1}"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
        out.append(name)
    return out


def _parse_csv(content, headerless=False):
    # utf-8-sig strips a leading BOM (europe.csv ships one on its first column).
    text = content.decode("utf-8-sig", "replace")
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return []
    width = max(len(r) for r in rows)
    if headerless:
        header = [f"col_{i + 1}" for i in range(width)]
        data = rows
    else:
        header = _sanitize_header(rows[0])
        for i in range(len(header), width):  # pad if any data row is wider
            header.append(f"col_{i + 1}")
        data = rows[1:]
    out = []
    for r in data:
        rec = {}
        for i, name in enumerate(header):
            val = r[i] if i < len(r) else None
            rec[name] = val if (val is not None and val != "") else None
        out.append(rec)
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id.removeprefix(f"{SLUG}-")
    cfg = ENTITY_CONFIG[entity]
    if cfg["mode"] == "gateway":
        url = f"https://{cfg['domain']}.execute-api.eu-central-1.amazonaws.com/web/url"
        resp = _fetch(url, params={"folder": "", "file_name": "latest.csv"})
        headerless = False
    else:
        path = quote(cfg["path"], safe="/")
        url = f"https://raw.githubusercontent.com/globaldothealth/{cfg['repo']}/{cfg['ref']}/{path}"
        resp = _fetch(url)
        headerless = cfg.get("headerless", False)
    rows = _parse_csv(resp.content, headerless=headerless)
    if not rows:
        raise RuntimeError(f"{asset}: parsed 0 rows from {url}")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_CONFIG
]
