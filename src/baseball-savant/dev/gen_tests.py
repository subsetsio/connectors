import json, os

SLUG = "baseball-savant"
OUT = "tests"

# slug -> (id_col, player_type_values_or_None)
BOARDS = {
    "statcast": ("player_id", ["batter", "pitcher"]),
    "expected_statistics": ("player_id", ["batter", "pitcher"]),
    "batted-ball": ("id", ["batter", "pitcher"]),
    "percentile-rankings": ("player_id", ["batter", "pitcher"]),
    "swing-take": ("player_id", None),
    "bat-tracking": ("id", ["batter", "pitcher"]),
    "pitch-arsenal-stats": ("player_id", ["pitcher"]),
    "pitch-arsenals": ("pitcher", None),
    "pitch-movement": ("pitcher_id", None),
    "pitch-tempo": ("entity_id", None),
    "active-spin": ("entity_id", None),
    "pitcher-arm-angles": ("pitcher", None),
    "sprint_speed": ("player_id", None),
    "running_splits": ("player_id", None),
    "outs_above_average": ("player_id", ["Fielder"]),
    "catch_probability": ("player_id", None),
    "outfield_jump": ("resp_fielder_id", None),
    "arm-strength": ("player_id", ["Fielder"]),
    "catcher-framing": ("id", ["Cat"]),
    "poptime": ("entity_id", None),
    "catcher-blocking": ("player_id", None),
    "catcher-throwing": ("player_id", None),
    "baserunning-run-value": ("player_id", None),
    "basestealing-run-value": ("player_id", None),
}

def spec_id(slug):
    return f"{SLUG}-{slug.replace('_', '-')}"

for slug, (idcol, ptypes) in BOARDS.items():
    sid = spec_id(slug)
    tests = [
        {"not_null": idcol,
         "reason": f"every Statcast leaderboard row is keyed to a player/entity id ({idcol}); a null id is a parse/column-shift bug on our side",
         "certainty": 95},
        {"column_type": {"col": idcol, "type": "integer"},
         "reason": "MLBAM player/entity ids are integers; our column-wise coercion types an all-numeric id column as int",
         "certainty": 90},
        {"column_type": {"col": "_requested_year", "type": "integer"},
         "reason": "fetch tags each row with the requested season as an int (or null for snapshot boards that ignore the year param)",
         "certainty": 90},
        {"between": {"col": "_requested_year", "lo": 2015, "hi": "current_year()"},
         "reason": "we only request seasons from the Statcast era (2015) to the current year; nulls (snapshot boards) are skipped by the check",
         "certainty": 85},
        {"row_count": {"min": 20},
         "reason": "a season-level board over the 2015-present era should always carry at least a few dozen qualified players; far fewer means a fetch/skip regression",
         "certainty": 75,
         "severity": "warn"},
    ]
    if ptypes:
        tests.append({
            "enum": {"col": "_player_type", "values": ptypes},
            "reason": "fetch tags each row with the perspective it was requested under; the value set is fixed by our config",
            "certainty": 95,
        })
    doc = {"spec_id": sid, "status": "active", "tests": tests}
    with open(os.path.join(OUT, f"{sid}.yaml"), "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")

# statcast pitch-by-pitch firehose
sid = f"{SLUG}-statcast-pitches"
doc = {
    "spec_id": sid,
    "status": "active",
    "tests": [
        {"not_null": "game_date",
         "reason": "every pitch belongs to a game on a date; read_csv_auto over the Savant pitch CSV always populates game_date",
         "certainty": 90},
        {"column_type": {"col": "game_date", "type": "date"},
         "reason": "game_date is an ISO yyyy-mm-dd; DuckDB read_csv_auto should infer a DATE",
         "certainty": 70,
         "severity": "warn"},
        {"not_null": "pitcher",
         "reason": "type=details pitch rows always carry the pitcher MLBAM id",
         "certainty": 90},
        {"column_type": {"col": "pitcher", "type": "integer"},
         "reason": "pitcher is an MLBAM id (integer)",
         "certainty": 85},
        {"not_null": "batter",
         "reason": "type=details pitch rows always carry the batter MLBAM id",
         "certainty": 90},
        {"at_most": {"col": "game_date", "expr": "today"},
         "reason": "no pitch can be thrown in the future",
         "certainty": 98,
         "points_outward": True},
        {"between": {"col": "release_speed", "lo": 20, "hi": 110},
         "reason": "MLB pitch release speed in mph spans roughly 40-105; 20-110 is a generous physical envelope (nulls allowed for unmeasured pitches)",
         "certainty": 85,
         "severity": "warn"},
        {"freshness": {"col": "game_date", "reaches": "today - 400d"},
         "reason": "a full-era re-pull should reach the most recent completed/ongoing season; a max older than ~400d means the firehose stopped early",
         "certainty": 80,
         "points_outward": True,
         "severity": "warn"},
        {"row_count": {"min": 100000},
         "reason": "the full 2015-present pitch corpus is millions of rows; a re-pull under 100k means windows were dropped",
         "certainty": 85,
         "severity": "warn"},
    ],
}
with open(os.path.join(OUT, f"{sid}.yaml"), "w") as f:
    json.dump(doc, f, indent=2)
    f.write("\n")

print("wrote", len(os.listdir(OUT)), "files")
