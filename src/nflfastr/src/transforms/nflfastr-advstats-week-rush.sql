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
    "carries",
    "rushing_yards_before_contact",
    "rushing_yards_before_contact_avg",
    "rushing_yards_after_contact",
    "rushing_yards_after_contact_avg",
    "rushing_broken_tackles",
    "receiving_broken_tackles"
FROM "nflfastr-advstats-week-rush"
