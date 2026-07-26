-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "income_group",
    "minimun_income_in_group",
    "number_of_filers",
    "percentage",
    "total_income_dollars_in_millions",
    "_" AS column,
    "avergae_income_per_filer"
FROM "nyc-open-data-ipc3-2nbm"
