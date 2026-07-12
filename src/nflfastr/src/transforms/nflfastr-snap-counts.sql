-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "game_id",
    "pfr_game_id",
    "season",
    "game_type",
    "week",
    "player",
    "pfr_player_id",
    "position",
    "team",
    "opponent",
    "offense_snaps",
    "offense_pct",
    "defense_snaps",
    "defense_pct",
    "st_snaps",
    "st_pct"
FROM "nflfastr-snap-counts"
