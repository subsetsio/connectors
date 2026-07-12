-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nflverse_game_id",
    CAST("old_game_id" AS BIGINT) AS old_game_id,
    "play_id",
    "possession_team",
    "offense_formation",
    "offense_personnel",
    "defenders_in_box",
    "defense_personnel",
    "number_of_pass_rushers",
    "players_on_play",
    "offense_players",
    "defense_players",
    "n_offense",
    "n_defense",
    "ngs_air_yards",
    "time_to_throw",
    "was_pressure",
    "route",
    "defense_man_zone_type",
    "defense_coverage_type",
    "offense_names",
    "defense_names",
    "offense_positions",
    "defense_positions",
    "offense_numbers",
    "defense_numbers"
FROM "nflfastr-pbp-participation"
