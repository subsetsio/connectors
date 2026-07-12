-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "season",
    "season_type",
    "week",
    "player_display_name",
    "player_position",
    "team_abbr",
    "efficiency",
    "percent_attempts_gte_eight_defenders",
    "avg_time_to_los",
    "rush_attempts",
    "rush_yards",
    "avg_rush_yards",
    "rush_touchdowns",
    "player_gsis_id",
    "player_first_name",
    "player_last_name",
    "player_jersey_number",
    "player_short_name",
    "expected_rush_yards",
    "rush_yards_over_expected",
    "rush_yards_over_expected_per_att",
    "rush_pct_over_expected"
FROM "nflfastr-ngs-rushing"
