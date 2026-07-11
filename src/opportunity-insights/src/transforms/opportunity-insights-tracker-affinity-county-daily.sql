-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "day",
    "countyfips",
    "freq",
    "spend_all",
    "provisional"
FROM "opportunity-insights-tracker-affinity-county-daily"
