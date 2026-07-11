-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "income_quartile",
    "share_jan2019"
FROM "opportunity-insights-tracker-affinity-income-shares-national-2019"
