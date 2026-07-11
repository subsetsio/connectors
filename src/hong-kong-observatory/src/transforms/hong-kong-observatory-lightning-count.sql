-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a recent lightning-count snapshot for the latest reporting window, not a historical strike-count series.
SELECT
    CAST("period_start" AS TIMESTAMP) AS period_start,
    CAST("period_end" AS TIMESTAMP) AS period_end,
    "type",
    "region",
    "count"
FROM "hong-kong-observatory-lightning-count"
