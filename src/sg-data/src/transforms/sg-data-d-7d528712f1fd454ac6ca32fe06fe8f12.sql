-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "occ_desc",
    "estab_size",
    "mthly_gross_wage_50_pctile",
    "mthly_basic_wage_50_pctile"
FROM "sg-data-d-7d528712f1fd454ac6ca32fe06fe8f12"
