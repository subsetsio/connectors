-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "game_id",
    "pfr_game_id",
    "season",
    "week",
    "game_type",
    "team",
    "opponent",
    "pfr_player_name",
    "pfr_player_id",
    "def_ints",
    "def_targets",
    "def_completions_allowed",
    "def_completion_pct",
    "def_yards_allowed",
    "def_yards_allowed_per_cmp",
    "def_yards_allowed_per_tgt",
    "def_receiving_td_allowed",
    "def_passer_rating_allowed",
    "def_adot",
    "def_air_yards_completed",
    "def_yards_after_catch",
    "def_times_blitzed",
    "def_times_hurried",
    "def_times_hitqb",
    "def_sacks",
    "def_pressures",
    "def_tackles_combined",
    "def_missed_tackles",
    "def_missed_tackle_pct"
FROM "nflfastr-advstats-week-def"
