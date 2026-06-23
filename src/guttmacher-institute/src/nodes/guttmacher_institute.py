"""Guttmacher Institute connector — public-use datasets hosted on OSF.

Guttmacher decommissioned its data.guttmacher.org Data Center; its public
datasets now live as OSF project nodes owned by the "Guttmacher Institute"
OSF account. Each rank-accepted node (see src/constants.py) ships one primary
public-use CSV table under its osfstorage tree (alongside Stata/SPSS/SAS/R
format variants and an xlsx codebook).

Fetch shape: stateless full re-pull (shape 1). The corpus is a handful of
small CSVs (~100KB–24MB each); re-fetching every node in full each run is
trivial, so there is no watermark/cursor/state. For each node we walk its
osfstorage tree, pick the single largest .csv file — which is reliably the
current release's primary table (newer releases carry more cumulative rows
than the archived copies under "Older releases") — and save its bytes raw as
CSV. The SQL transform reads that CSV directly (DuckDB read_csv_auto) and is
the correctness gate: it types the columns and fails loudly on a malformed or
empty pull.
"""

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_file, transient_retry

SLUG = "guttmacher-institute"
OSF_API = "https://api.osf.io/v2"


@transient_retry()
def _get_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _list_csv_files(osf_node: str) -> list[tuple[int, str, str]]:
    """Recurse a node's osfstorage tree; return (size, name, download_url) for
    every .csv file found, at any depth."""
    found: list[tuple[int, str, str]] = []
    stack = [f"{OSF_API}/nodes/{osf_node}/files/osfstorage/?page[size]=100"]
    while stack:
        url = stack.pop()
        while url:
            doc = _get_json(url)
            for item in doc.get("data", []):
                attrs = item.get("attributes", {})
                name = attrs.get("name") or ""
                if attrs.get("kind") == "folder":
                    related = (
                        item.get("relationships", {})
                        .get("files", {})
                        .get("links", {})
                        .get("related", {})
                        .get("href")
                    )
                    if related:
                        stack.append(related)
                elif name.lower().endswith(".csv"):
                    found.append((
                        attrs.get("size") or 0,
                        name,
                        item.get("links", {}).get("download"),
                    ))
            url = doc.get("links", {}).get("next")
    return found


def _to_utf8(content: bytes) -> bytes:
    """Normalize CSV bytes to UTF-8. Clean UTF-8 files pass through the first
    (strict) decode unchanged; Windows-encoded exports (e.g. the GSRHE survey,
    a Dynata cp1252 dump with smart quotes/accents in free-text answers) decode
    via cp1252 so DuckDB's read_csv_auto, which only accepts UTF-8, can read
    them. latin-1 is the never-fail fallback."""
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return content.decode(enc).encode("utf-8")
        except UnicodeDecodeError:
            continue
    return content.decode("latin-1").encode("utf-8")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    osf_node = node_id[len(f"{SLUG}-"):]

    csvs = _list_csv_files(osf_node)
    if not csvs:
        # A node with no CSV is a contract violation (the entity union was
        # vetted to only contain CSV-bearing nodes) — fail loudly, don't
        # publish an empty asset.
        raise AssertionError(f"{node_id}: OSF node {osf_node} exposes no .csv file")

    # Largest CSV = the current release's primary table.
    size, name, download_url = max(csvs, key=lambda t: t[0])
    if not download_url:
        raise AssertionError(f"{node_id}: primary CSV {name!r} has no download link")

    content = _to_utf8(_download(download_url))
    save_raw_file(content, asset, extension="csv")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published table per dataset. The CSV is saved raw; the transform is a
# thin pass that DuckDB types via read_csv_auto. SELECT * publishes the table
# as-is — column casting/cleanup beyond this would require per-dataset schema
# knowledge that belongs downstream, not in this fetch-and-publish stage.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=f'SELECT * FROM "{spec.id}"',
    )
    for spec in DOWNLOAD_SPECS
]
