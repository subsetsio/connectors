"""Baseball Savant (MLB Statcast) leaderboards.

**Leaderboards** (24 specs) — season-level Statcast aggregate boards served as
CSV at `/leaderboard/<slug>?...&csv=true`. Each board has its own column list,
so each is its own published table. The Statcast era runs 2015-present; we
request every season `2015..current_year` and keep what comes back. Boards that
honor the `year` param return distinct rows per season (and 0 rows for seasons
before the metric existed, which we skip); a few boards ignore `year` and return
a single fixed snapshot. We detect the latter generically by content-dedup: if
the same CSV body comes back for more than one requested season, the season is
unknown (`_requested_year` = null); otherwise each season is tagged with the
season it was requested for. Several boards expose both batter and pitcher
perspectives; we fetch both and tag `_player_type`. Stateless full re-pull
every run (small payloads), overwrite downstream.

This is a *parametric* family: one config-driven `fetch_leaderboard` drives all
24 boards from a config row, so they correctly co-locate in one file. Leaderboard
CSV values are coerced column-wise to int/float/str (empty -> null) so the raw
ndjson carries proper types. SQL transforms are thin parse-and-publish passes.
"""

from collections import defaultdict
from datetime import datetime, timezone
import csv
import hashlib
import io

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import SLUG, STATCAST_ERA_START_YEAR, _fetch_csv_text


# ---------------------------------------------------------------------------
# CSV parsing + column-wise type coercion
# ---------------------------------------------------------------------------

def _parse_csv(text: str) -> list[dict]:
    # Strip the UTF-8 BOM first: a leading ﻿ before the opening quote stops
    # csv from recognizing the quoted "last_name, first_name" composite field,
    # which would split it on the inner comma and shift every column.
    if text and text[0] == "﻿":
        text = text[1:]
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames:
        reader.fieldnames = [(f or "").strip() for f in reader.fieldnames]
    return [dict(row) for row in reader]


def _is_int(v) -> bool:
    try:
        int(v)
        return True
    except (TypeError, ValueError):
        return False


def _is_float(v) -> bool:
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


def _typed_rows(rows: list[dict]) -> list[dict]:
    """Coerce every column to a single type (int/float/str) across all rows;
    empty strings become null. Per-column typing keeps ndjson batches unionable."""
    if not rows:
        return []
    cols: list[str] = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    coltype: dict[str, str] = {}
    for c in cols:
        nonempty = [r.get(c) for r in rows if r.get(c) not in (None, "")]
        if not nonempty:
            coltype[c] = "str"
        elif all(_is_int(v) for v in nonempty):
            coltype[c] = "int"
        elif all(_is_float(v) for v in nonempty):
            coltype[c] = "float"
        else:
            coltype[c] = "str"
    out = []
    for r in rows:
        d = {}
        for c in cols:
            v = r.get(c)
            if v is None or v == "":
                d[c] = None
            elif coltype[c] == "int":
                d[c] = int(v)
            elif coltype[c] == "float":
                d[c] = float(v)
            else:
                d[c] = v
        out.append(d)
    return out


# ---------------------------------------------------------------------------
# Leaderboards
# ---------------------------------------------------------------------------

# slug -> (query_template, type_values, tag_player_type)
#   query_template: format string with {y} (season) and optionally {type}.
#   type_values: substituted into {type}; [None] when the board has no type axis.
#   tag_player_type: True when the type token is a real player perspective worth
#                    publishing as a column (batter/pitcher/Fielder/Cat).
_LEADERBOARDS: dict[str, tuple[str, list, bool]] = {
    "statcast": ("type={type}&year={y}", ["batter", "pitcher"], True),
    "expected_statistics": ("type={type}&year={y}", ["batter", "pitcher"], True),
    "batted-ball": ("type={type}&year={y}", ["batter", "pitcher"], True),
    "percentile-rankings": ("type={type}&year={y}", ["batter", "pitcher"], True),
    # swing-take returns 0 rows when a `type` is passed; the unfiltered board
    # already covers all players. year is honored.
    "swing-take": ("year={y}", [None], False),
    "bat-tracking": ("attackZone=&batSide=&type={type}&year={y}", ["batter", "pitcher"], True),
    "pitch-arsenal-stats": ("type={type}&year={y}", ["pitcher"], True),
    "pitch-arsenals": ("year={y}&type=avg_speed", [None], False),
    "pitch-movement": ("year={y}", [None], False),
    "pitch-tempo": ("year={y}", [None], False),
    "active-spin": ("year={y}_spin-based", [None], False),
    "pitcher-arm-angles": ("year={y}", [None], False),
    "sprint_speed": ("year={y}&position=&team=&min_season={y}&max_season={y}", [None], False),
    "running_splits": ("type=raw&bats=&year={y}&position=&team=&min=5", [None], False),
    "outs_above_average": ("type={type}&year={y}", ["Fielder"], True),
    # catch_probability returns 0 rows when type=Fielder is passed; unfiltered
    # board returns the outfielder catch-probability leaderboard. year honored.
    "catch_probability": ("year={y}", [None], False),
    "outfield_jump": ("year={y}", [None], False),
    "arm-strength": ("type={type}&year={y}", ["Fielder"], True),
    "catcher-framing": ("type={type}&year={y}", ["Cat"], True),
    "poptime": ("year={y}", [None], False),
    "catcher-blocking": ("year={y}", [None], False),
    "catcher-throwing": ("year={y}", [None], False),
    "baserunning-run-value": ("year={y}", [None], False),
    "basestealing-run-value": ("year={y}", [None], False),
}


# Spec ids are hyphenated (`f"baseball-savant-{entity_id.replace('_','-')}"`), but
# the URL slugs preserve underscores (e.g. `expected_statistics`). Map back so the
# fetch fn recovers the exact URL slug from the node id it is handed.
_SPEC_TO_URLSLUG = {
    f"{SLUG}-{eid.replace('_', '-')}": eid for eid in _LEADERBOARDS
}


def fetch_leaderboard(node_id: str) -> None:
    slug = _SPEC_TO_URLSLUG[node_id]
    template, type_values, tag_player_type = _LEADERBOARDS[slug]
    current_year = datetime.now(timezone.utc).year
    years = list(range(STATCAST_ERA_START_YEAR, current_year + 1))

    board_rows: list[dict] = []
    for tval in type_values:
        # year -> (content_hash, parsed_rows) for non-empty responses
        per_year: list[tuple[int, str, list[dict]]] = []
        for y in years:
            query = template.format(y=y, type=tval if tval is not None else "")
            url = f"https://baseballsavant.mlb.com/leaderboard/{slug}?{query}&csv=true"
            text = _fetch_csv_text(url)
            if text is None:
                continue
            rows = _parse_csv(text)
            if not rows:
                continue
            h = hashlib.md5(text.encode("utf-8")).hexdigest()
            per_year.append((y, h, rows))

        # group by content hash: a hash seen for >1 distinct year means the board
        # ignored the year param (single snapshot) -> season is unknown.
        hash_years: dict[str, list[int]] = defaultdict(list)
        hash_rows: dict[str, list[dict]] = {}
        for y, h, rows in per_year:
            hash_years[h].append(y)
            hash_rows[h] = rows
        for h, yrs in hash_years.items():
            req_year = yrs[0] if len(set(yrs)) == 1 else None
            for r in hash_rows[h]:
                rr = dict(r)
                rr["_requested_year"] = req_year
                if tag_player_type:
                    rr["_player_type"] = tval
                board_rows.append(rr)

    if not board_rows:
        raise RuntimeError(f"{node_id}: no leaderboard rows fetched across {years}")

    save_raw_ndjson(_typed_rows(board_rows), node_id)


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------

# Named without the `_SPECS` suffix so `load_nodes()` does NOT discover them
# directly: the canonical `baseball_savant.py` module concatenates these with the
# statcast family into the single DOWNLOAD_SPECS / TRANSFORM_SPECS the harness
# introspects. Discovering both here and there would duplicate every node id.
LEADERBOARD_DOWNLOADS = [
    NodeSpec(id=f"{SLUG}-{slug.replace('_', '-')}", fn=fetch_leaderboard, kind="download")
    for slug in _LEADERBOARDS
]

LEADERBOARD_TRANSFORMS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in LEADERBOARD_DOWNLOADS
]
