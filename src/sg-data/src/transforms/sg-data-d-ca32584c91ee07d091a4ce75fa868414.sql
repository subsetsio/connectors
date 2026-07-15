-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "residential_status",
    "seasonally_adj_unemp_rate",
    "non_seasonally_adj_unemp_rate"
FROM "sg-data-d-ca32584c91ee07d091a4ce75fa868414"
