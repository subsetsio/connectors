"""nflfastR / nflverse connector.

Mechanism: bulk parquet assets published on the nflverse/nflverse-data GitHub
releases (one release tag per dataset family). For each entity we list the
release's assets, keep the parquet files whose season-stripped stem equals the
entity id (one per season, or a single whole-corpus file), download them, and
union them by name into a single combined raw parquet.

Schemas drift slightly across seasons (columns added in later years, an int
column that became a double), so the files are unioned with DuckDB
`union_by_name=true`, which aligns columns by name and promotes numeric types.
The union is streamed in bounded batches to keep memory flat even for the
372-column play-by-play corpus (~1.3M rows).

Fetch shape: stateless full re-pull. The whole corpus is a few GB and the
nflverse releases are rebuilt nightly during the season with revisions to prior
weeks; trusting a stored watermark would silently skip those revisions. Each run
re-downloads every season and overwrites — freshness gating is the maintain
step's job, not ours.
"""

from __future__ import annotations

import os
import re
import tempfile

import duckdb

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)
from constants import ENTITY_IDS, ENTITY_TAGS, REPO

_API = f"https://api.github.com/repos/{REPO}/releases/tags"
_DL = f"https://github.com/{REPO}/releases/download"
_BATCH_ROWS = 20_000  # cap rows per streamed batch → bounded memory


def _stem(asset_name: str) -> str:
    """Filename stem with the season-year token removed — must match the entity
    ids produced by collect (e.g. 'play_by_play_2025.parquet' -> 'play_by_play',
    'ngs_2021_passing.parquet' -> 'ngs_passing')."""
    n = asset_name[:-len(".parquet")] if asset_name.endswith(".parquet") else asset_name
    n = re.sub(r"_?(?:19|20)\d\d", "", n)
    n = re.sub(r"__+", "_", n).strip("_")
    return n


def _gh_headers() -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


@transient_retry()
def _release_parquet_assets(tag: str) -> list[str]:
    """Parquet asset filenames for a release tag (via the GitHub releases API)."""
    resp = get(f"{_API}/{tag}", headers=_gh_headers(), timeout=(10.0, 60.0))
    resp.raise_for_status()
    return [a["name"] for a in resp.json().get("assets", []) if a["name"].endswith(".parquet")]


@transient_retry()
def _download_to(path: str, url: str) -> None:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    with open(path, "wb") as fh:
        fh.write(resp.content)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity = node_id[len("nflfastr-"):].replace("-", "_")
    tag = ENTITY_TAGS[entity]

    all_assets = _release_parquet_assets(tag)
    files = sorted(name for name in all_assets if _stem(name) == entity)
    if not files:
        # A missing entity means the release layout changed — fail loudly so the
        # run records it rather than silently publishing nothing.
        raise AssertionError(
            f"{node_id}: no parquet assets with stem '{entity}' in release "
            f"'{tag}' (saw {all_assets[:8]})"
        )

    with tempfile.TemporaryDirectory() as tmp:
        local = []
        for name in files:
            dst = os.path.join(tmp, name)
            _download_to(dst, f"{_DL}/{tag}/{name}")
            local.append(dst)

        con = duckdb.connect()
        try:
            rel = con.sql(f"SELECT * FROM read_parquet({local!r}, union_by_name=true)")
            reader = rel.fetch_record_batch(rows_per_batch=_BATCH_ROWS)
            with raw_parquet_writer(asset, reader.schema) as writer:
                for batch in reader:
                    if batch.num_rows:
                        writer.write_batch(batch)
        finally:
            con.close()


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"nflfastr-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Per-subset grain / observation-period declarations. Keyed by DOWNLOAD spec id.
# Keys are declared only for the well-known nflverse grains we are confident are
# unique; the observation period is the `season` column (the ETL `loaded`/
# `birth_date`/`dt` timestamps are freshness metadata, not the row's period).
GRAIN = {
    # canonical unique grains
    "nflfastr-play-by-play": {"key": ("game_id", "play_id"), "temporal": "season"},
    "nflfastr-pbp-participation": {"key": ("nflverse_game_id", "play_id")},  # no period column
    "nflfastr-games": {"key": ("game_id",), "temporal": "season"},
    "nflfastr-players": {"key": ("gsis_id",)},  # player dimension, timeless
    "nflfastr-ftn-charting": {"key": ("ftn_play_id",), "temporal": "season"},
    "nflfastr-officials": {"key": ("game_id", "official_id"), "temporal": "season"},
    "nflfastr-snap-counts": {"key": ("game_id", "pfr_player_id"), "temporal": "season"},
    "nflfastr-ngs-passing": {"key": ("season", "season_type", "week", "player_gsis_id"), "temporal": "season"},
    "nflfastr-ngs-receiving": {"key": ("season", "season_type", "week", "player_gsis_id"), "temporal": "season"},
    "nflfastr-ngs-rushing": {"key": ("season", "season_type", "week", "player_gsis_id"), "temporal": "season"},
    "nflfastr-qbr-season-level": {"key": ("season", "season_type", "player_id"), "temporal": "season"},
    "nflfastr-qbr-week-level": {"key": ("season", "season_type", "game_id", "player_id"), "temporal": "season"},
    "nflfastr-stats-player-reg": {"key": ("player_id", "season", "season_type"), "temporal": "season"},
    "nflfastr-stats-player-post": {"key": ("player_id", "season", "season_type"), "temporal": "season"},
    "nflfastr-stats-player-regpost": {"key": ("player_id", "season", "season_type"), "temporal": "season"},
    "nflfastr-stats-player-week": {"key": ("player_id", "season", "week", "season_type"), "temporal": "season"},
    "nflfastr-stats-team-reg": {"key": ("season", "team", "season_type"), "temporal": "season"},
    "nflfastr-stats-team-post": {"key": ("season", "team", "season_type"), "temporal": "season"},
    "nflfastr-stats-team-regpost": {"key": ("season", "team", "season_type"), "temporal": "season"},
    "nflfastr-stats-team-week": {"key": ("season", "week", "team", "season_type"), "temporal": "season"},
    # period only (grain not confidently unique: multi-team splits / nullable ids)
    "nflfastr-advstats-season-def": {"temporal": "season"},
    "nflfastr-advstats-season-pass": {"temporal": "season"},
    "nflfastr-advstats-season-rec": {"temporal": "season"},
    "nflfastr-advstats-season-rush": {"temporal": "season"},
    "nflfastr-advstats-week-def": {"temporal": "season"},
    "nflfastr-advstats-week-pass": {"temporal": "season"},
    "nflfastr-advstats-week-rec": {"temporal": "season"},
    "nflfastr-advstats-week-rush": {"temporal": "season"},
    "nflfastr-combine": {"temporal": "season"},
    "nflfastr-depth-charts": {"temporal": "season"},
    "nflfastr-draft-picks": {"temporal": "season"},
    "nflfastr-historical-contracts": {"temporal": "year_signed"},
    "nflfastr-injuries": {"temporal": "season"},
    "nflfastr-roster": {"temporal": "season"},
    "nflfastr-roster-weekly": {"temporal": "season"},
    "nflfastr-trades": {"temporal": "season"},
}

# One published Delta table per subset. The raw parquet is already clean, typed,
# self-describing nflverse data, so the transform is a typed pass-through: it is
# the correctness gate (fails loudly if raw is missing/empty/unreadable) without
# reshaping data that is already in the right shape.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=f'SELECT * FROM "{spec.id}"',
        key=GRAIN.get(spec.id, {}).get("key"),
        temporal=GRAIN.get(spec.id, {}).get("temporal"),
    )
    for spec in DOWNLOAD_SPECS
]
