"""Baseball Savant — canonical node module.

The connector's fetches are split across two sibling modules by retrieval shape:

  - `leaderboards.py` — the 24 season-level Statcast leaderboard boards (CSV,
    per-season, column-wise typed ndjson).
  - `statcast.py` — the pitch-by-pitch firehose (date-windowed, gzipped CSV,
    DuckDB-typed at transform time).

Each is its own file because the fetch bodies are genuinely distinct. This module
is the single place the harness introspects (`src/nodes/<slug>.py`): it unions both
families into the one `DOWNLOAD_SPECS` / `TRANSFORM_SPECS` pair that defines the DAG.

The sibling modules deliberately expose their spec lists under names that do NOT
end in `_SPECS`, so `load_nodes()` only discovers the unioned lists here — a node
id is registered exactly once.
"""

# Import the fetch callables into this module's namespace too: the harness
# validates that every download spec's `fn` is a top-level attribute of the
# introspected module (`getattr(module, fn.__name__) is fn`).
from nodes.leaderboards import (
    LEADERBOARD_DOWNLOADS,
    LEADERBOARD_TRANSFORMS,
    fetch_leaderboard,
)
from nodes.statcast import (
    STATCAST_DOWNLOADS,
    STATCAST_TRANSFORMS,
    fetch_statcast_pitches,
)

DOWNLOAD_SPECS = LEADERBOARD_DOWNLOADS + STATCAST_DOWNLOADS

TRANSFORM_SPECS = LEADERBOARD_TRANSFORMS + STATCAST_TRANSFORMS
