import json, os
S=json.load(open(os.path.join("dev","schemas.json")))

INT={"int32","int64"}
def floor(rows_one,nfiles):
    return max(50, int(rows_one*max(1,nfiles)*0.3))

# entities with no season column -> alternate non-null key
NO_SEASON_KEY={"depth_charts":"team","players":"gsis_id","historical_contracts":"player"}

def yaml_for(ent, info):
    sid=f"nflfastr-{ent.replace('_','-')}"
    cols=info["cols"]
    has_season = ("season" in cols and cols["season"] in INT)
    lines=[f"spec_id: {sid}", "status: active", "tests:"]
    key = "season" if has_season else NO_SEASON_KEY.get(ent, list(cols)[0])
    lines.append(f"  - not_null: {key}")
    if has_season:
        lines.append("  - column_type: {col: season, type: integer}")
        lines.append("  - at_most: {col: season, expr: current_year()}")
        lines.append("    certainty: 85")
        lines.append("    points_outward: true")
        lines.append("    severity: warn")
        lines.append("    reason: nflverse seasons never exceed the current year; a higher value means a parsing/union error")
    lines.append(f"  - row_count: {{min: {floor(info['rows_one'],info['nfiles'])}}}")
    lines.append("    certainty: 70")
    lines.append(f"    reason: conservative floor (~0.3x of {info['nfiles']} season file(s) at ~{info['rows_one']} rows each); a lower count means dropped files")
    return sid, "\n".join(lines)+"\n"

# richer hand-authored beliefs for the two flagships
HAND={
 "play_by_play": """spec_id: nflfastr-play-by-play
status: active
tests:
  - not_null: game_id
  - not_null: season
  - column_type: {col: season, type: integer}
  - between: {col: season, lo: 1999, hi: current_year()}
    certainty: 95
    reason: nflfastR play-by-play starts in 1999 and runs to the current season
  - unique: [game_id, play_id]
    certainty: 80
    reason: one row per play within a game; dupes mean a season file was unioned twice
  - row_count: {min: 800000}
    certainty: 85
    reason: ~48k plays/season x 27 seasons; well under 1.3M actual
""",
 "games": """spec_id: nflfastr-games
status: active
tests:
  - not_null: game_id
  - unique: game_id
    certainty: 95
    reason: schedules has exactly one row per game
  - not_null: season
  - column_type: {col: season, type: integer}
  - between: {col: season, lo: 1999, hi: current_year()}
    certainty: 90
  - row_count: {min: 6000}
    certainty: 85
    reason: ~285 games/season x 27 seasons
""",
}

os.makedirs("tests", exist_ok=True)
n=0
for ent,info in S.items():
    sid=f"nflfastr-{ent.replace('_','-')}"
    if ent in HAND:
        content=HAND[ent]
    else:
        _,content=yaml_for(ent,info)
    open(os.path.join("tests",f"{sid}.yaml"),"w").write(content)
    n+=1
print("wrote",n,"yaml files")
