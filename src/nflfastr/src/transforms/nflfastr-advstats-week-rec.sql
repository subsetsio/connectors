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
    "rushing_broken_tackles",
    "receiving_broken_tackles",
    "passing_drops",
    "passing_drop_pct",
    "receiving_drop",
    "receiving_drop_pct",
    "receiving_int",
    "receiving_rat"
FROM "nflfastr-advstats-week-rec"
