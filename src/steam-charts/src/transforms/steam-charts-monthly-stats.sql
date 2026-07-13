-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Monthly statistics are grouped by Steam Charts' period labels; treat period_label as the source month label and fetched_at as the collection timestamp.
SELECT
    "app_id",
    "app_name",
    "period_label",
    "period_start",
    "is_last_30_days",
    "avg_players",
    "gain",
    "percent_gain",
    "peak_players",
    "fetched_at"
FROM "steam-charts-monthly-stats"
