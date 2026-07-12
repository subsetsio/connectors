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
    "passing_drops",
    "passing_drop_pct",
    "receiving_drop",
    "receiving_drop_pct",
    "passing_bad_throws",
    "passing_bad_throw_pct",
    "times_sacked",
    "times_blitzed",
    "times_hurried",
    "times_hit",
    "times_pressured",
    "times_pressured_pct",
    "def_times_blitzed",
    "def_times_hurried",
    "def_times_hitqb"
FROM "nflfastr-advstats-week-pass"
