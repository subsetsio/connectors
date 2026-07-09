"""Czech Statistical Office (ČSÚ / CZSO) open-data connector.

Catalog connector over CZSO's CKAN-style open-data API. Each rank-accepted
dataset is a single full CSV published at csu.gov.cz, discovered via the CKAN
`package_show` resource list on vdb.czso.cz. The CSVs are long-format
observation tables (one row per coded observation) with per-dataset column
sets; encoding is UTF-8, comma-delimited, double-quoted, header present
(verified across diverse datasets while probing).

Fetch shape: **stateless full re-pull** (decision shape 1). Each dataset is a
single CSV of at most a few tens of MB and there is no incremental query
filter on the CKAN API, so every run re-fetches the whole CSV and overwrites.
Freshness gating is the maintain step's job.

Raw format: the CSV is normalized to UTF-8 and saved as a file (`save_raw_file`,
extension "csv"). CZSO serves a mix of UTF-8 and CP1250 (Windows Central
European) CSVs — and DuckDB's CSV sniffer hard-fails on non-UTF-8 bytes — so the
fetch fn decodes (utf-8 → cp1250 → latin-1) and re-encodes as clean UTF-8 before
saving. A few datasets ship the CSV inside a ZIP; those are unpacked here too.
Column sets differ per dataset, so the transform is a generic passthrough that
lets DuckDB infer types from each dataset's own CSV — a thin parse/type pass,
the only scalable shape across 200+ heterogeneous tables.
"""

import io
import zipfile

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_file,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "czech-statistical-office"
CKAN_BASE = "https://vdb.czso.cz/pll/eweb"

# spec id (lossy: lower + '_'->'-') back to the source's original dataset id.
_SPEC_TO_ENTITY = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


@transient_retry()  # 6 attempts, exponential backoff over transient/429/5xx
def _package_show(entity_id: str) -> dict:
    resp = get(
        f"{CKAN_BASE}/package_show",
        params={"id": entity_id},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()["result"]


@transient_retry()
def _download_csv(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _to_utf8_csv(content: bytes, url: str, resource_format: str) -> bytes:
    """Return clean UTF-8 CSV bytes from a downloaded resource.

    Unpacks a ZIP wrapper (a few datasets ship the CSV zipped), then decodes the
    CSV with the right charset — CZSO mixes UTF-8 and CP1250 — and re-encodes as
    UTF-8 so DuckDB's sniffer (which hard-fails on non-UTF-8) reads it cleanly.
    """
    fmt = (resource_format or "").lower()
    is_zip = "zip" in fmt or url.lower().split("?")[0].endswith(".zip")
    if is_zip or content[:2] == b"PK":
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            if not members:
                raise RuntimeError(f"zip has no .csv member: {zf.namelist()[:5]}")
            content = zf.read(members[0])

    if content[:3] == b"\xef\xbb\xbf":  # strip UTF-8 BOM
        content = content[3:]
    for enc in ("utf-8", "cp1250", "latin-1"):
        try:
            text = content.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:  # pragma: no cover - latin-1 never raises, here for clarity
        text = content.decode("utf-8", errors="replace")
    return text.encode("utf-8")


def _pick_csv_resource(resources: list) -> dict:
    """Pick the dataset's CSV distribution. Every probed dataset exposes exactly
    one text/csv resource; prefer an explicit csv format, else the sole
    resource. Raise loudly if there's nothing CSV-shaped to fetch."""
    csv_res = [
        r for r in resources
        if "csv" in (r.get("format") or "").lower()
        or (r.get("url") or "").lower().split("?")[0].endswith(".csv")
    ]
    if csv_res:
        return csv_res[0]
    if len(resources) == 1:
        return resources[0]
    raise RuntimeError(
        f"no CSV resource among {len(resources)} resources: "
        f"{[r.get('format') for r in resources]}"
    )


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = _SPEC_TO_ENTITY[node_id]

    rec = _package_show(entity_id)
    resources = rec.get("resources") or []
    if not resources:
        raise RuntimeError(f"{entity_id}: package_show returned no resources")

    res = _pick_csv_resource(resources)
    url = res.get("url") or ""
    if not url.startswith("http"):
        raise RuntimeError(f"{entity_id}: resource has no usable URL: {url!r}")
    content = _download_csv(url)
    content = _to_utf8_csv(content, url, res.get("format", ""))
    save_raw_file(content, asset, extension="csv")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
