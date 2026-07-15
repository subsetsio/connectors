-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "total_gov_operating_rev",
    "iras_collection"
FROM "sg-data-d-585cd3479aa16f2b741ac67fa0497628"
