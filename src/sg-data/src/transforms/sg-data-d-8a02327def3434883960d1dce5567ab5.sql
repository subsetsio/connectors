-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "residential_status",
    "seasonally_adj_unemp",
    "non_seasonally_adj_unemp"
FROM "sg-data-d-8a02327def3434883960d1dce5567ab5"
