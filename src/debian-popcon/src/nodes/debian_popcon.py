"""Debian Popularity Contest — package usage statistics.

Source: https://popcon.debian.org/ — a community project that aggregates,
per Debian package, how many reporting installations have it installed
(`inst`), use it regularly (`vote`), have it installed-but-unused (`old`),
upgraded it recently (`recent`), or sent an incomplete entry (`no-files`).

Each subset is one aggregation "view" published as a stable bulk text file
(we fetch the `.gz` variant). The five `by_*` files in any one directory are
the SAME table re-sorted, so we fetch only `by_inst` per view:

  - packages            -> by_inst.gz          (one row per binary package)
  - source-packages     -> source/by_inst.gz   (per source package, summed)
  - source-packages-max -> sourcemax/by_inst.gz (per source package, max)
  - maintainers         -> maint/by_inst.gz    (per maintainer, summed)

Stateless full re-pull: each view is a small whole-corpus snapshot popcon
regenerates ~daily, re-fetched in full every run and overwritten. No
incremental filter exists and none is needed.

File format (documented only in each file's `#` comment header, which is
stable): whitespace-delimited fixed-width rows
    rank  name  inst  vote  old  recent  no-files  [(maintainer)]
The `name` field contains spaces in the source/maintainer views ("Not in
sid", "Debian Gnome Maintainers"); the trailing `(maintainer)` column exists
only in the per-binary-package view. So the parser anchors on the right: pull
the optional parenthesized maintainer, then the trailing 5 integer metrics,
leaving rank as the head token and everything between as the name.
"""

import gzip

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

# spec id -> path under https://popcon.debian.org/ (.gz variant of by_inst)
VIEW_PATHS = {
    "debian-popcon-packages": "by_inst.gz",
    "debian-popcon-source-packages": "source/by_inst.gz",
    "debian-popcon-source-packages-max": "sourcemax/by_inst.gz",
    "debian-popcon-maintainers": "maint/by_inst.gz",
}

BASE_URL = "https://popcon.debian.org/"

# Generic raw schema shared by every view. `maintainer` is populated only for
# the per-binary-package view; null elsewhere.
SCHEMA = pa.schema([
    ("rank", pa.int64()),
    ("name", pa.string()),
    ("inst", pa.int64()),
    ("vote", pa.int64()),
    ("old", pa.int64()),
    ("recent", pa.int64()),
    ("no_files", pa.int64()),
    ("maintainer", pa.string()),
])


@transient_retry()
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _parse(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        s = line.rstrip()
        if not s or s.startswith("#") or s.lstrip().startswith("-"):
            continue  # blank, comment header, or the footer separator rule

        # Right-anchored: peel the optional trailing "(maintainer)".
        maintainer = None
        if s.endswith(")") and "(" in s:
            idx = s.rfind("(")
            maintainer = s[idx + 1:-1].strip() or None
            s = s[:idx].rstrip()

        toks = s.split()
        # rank + name(>=1 tok) + 5 metric ints
        if len(toks) < 7 or not toks[0].isdigit():
            continue
        name = " ".join(toks[1:-5])
        if name == "Total":  # the footer aggregate row
            continue
        inst, vote, old, recent, no_files = (int(t) for t in toks[-5:])
        rows.append({
            "rank": int(toks[0]),
            "name": name,
            "inst": inst,
            "vote": vote,
            "old": old,
            "recent": recent,
            "no_files": no_files,
            "maintainer": maintainer,
        })
    return rows


def fetch_view(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    content = _download(BASE_URL + VIEW_PATHS[node_id])
    text = gzip.decompress(content).decode("utf-8", "replace")
    rows = _parse(text)
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="debian-popcon-packages", fn=fetch_view, kind="download"),
    NodeSpec(id="debian-popcon-source-packages", fn=fetch_view, kind="download"),
    NodeSpec(id="debian-popcon-source-packages-max", fn=fetch_view, kind="download"),
    NodeSpec(id="debian-popcon-maintainers", fn=fetch_view, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="debian-popcon-packages-transform",
        deps=["debian-popcon-packages"],
        sql='''
            SELECT
                rank,
                name AS package,
                inst,
                vote,
                old,
                recent,
                no_files,
                maintainer
            FROM "debian-popcon-packages"
        ''',
    ),
    SqlNodeSpec(
        id="debian-popcon-source-packages-transform",
        deps=["debian-popcon-source-packages"],
        sql='''
            SELECT
                rank,
                name AS source_package,
                inst,
                vote,
                old,
                recent,
                no_files
            FROM "debian-popcon-source-packages"
        ''',
    ),
    SqlNodeSpec(
        id="debian-popcon-source-packages-max-transform",
        deps=["debian-popcon-source-packages-max"],
        sql='''
            SELECT
                rank,
                name AS source_package,
                inst,
                vote,
                old,
                recent,
                no_files
            FROM "debian-popcon-source-packages-max"
        ''',
    ),
    SqlNodeSpec(
        id="debian-popcon-maintainers-transform",
        deps=["debian-popcon-maintainers"],
        sql='''
            SELECT
                rank,
                name AS maintainer,
                inst,
                vote,
                old,
                recent,
                no_files
            FROM "debian-popcon-maintainers"
        ''',
    ),
]
