-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "housing_type",
    "dwelling_type",
    "tg_consumption_gwh"
FROM "sg-data-d-e8fb7c462d24dac06375c552a776988c"
