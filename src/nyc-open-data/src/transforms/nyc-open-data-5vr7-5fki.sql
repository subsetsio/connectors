-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "race",
    "mos_type",
    "ranklit",
    "sex",
    "appdate",
    "yearsonjob",
    "yearsonjob_bins"
FROM "nyc-open-data-5vr7-5fki"
