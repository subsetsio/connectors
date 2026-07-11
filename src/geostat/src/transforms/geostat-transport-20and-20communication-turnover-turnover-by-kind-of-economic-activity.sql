-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kind_economic_activity",
    "period",
    "value"
FROM "geostat-transport-20and-20communication-turnover-turnover-by-kind-of-economic-activity"
