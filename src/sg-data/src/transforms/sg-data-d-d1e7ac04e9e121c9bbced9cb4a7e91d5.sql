-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "occ_desc",
    "sex",
    "mthly_gross_wage_50_pctile",
    "mthly_basic_wage_50_pctile"
FROM "sg-data-d-d1e7ac04e9e121c9bbced9cb4a7e91d5"
