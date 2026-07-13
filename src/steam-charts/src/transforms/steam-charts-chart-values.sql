-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Chart values come from Steam Charts per-app chart JSON; the source does not document the exact chart aggregate represented by each value.
SELECT
    "app_id",
    "app_name",
    "observed_at",
    "players",
    "fetched_at"
FROM "steam-charts-chart-values"
