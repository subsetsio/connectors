-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "occ_desc",
    "estab_size1",
    "estab_size2",
    "age_grp1",
    "mthly_gross_wage_50_pctile",
    "mthly_basic_wage_50_pctile"
FROM "sg-data-d-db0e6e9b54364552dd9d2fc6a28f14f0"
