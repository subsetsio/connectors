-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table is a point-in-time catalog snapshot of Steam Charts metrics captured at fetch time; use fetched_at when comparing repeated runs.
SELECT
    "app_id",
    "name",
    "rank",
    "current_players",
    "peak_players_30d",
    "player_hours_30d",
    "source_page",
    "fetched_at"
FROM "steam-charts-games"
