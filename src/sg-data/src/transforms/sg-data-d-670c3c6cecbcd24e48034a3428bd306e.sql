-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "major_occ",
    "ind1",
    "occ_desc",
    "mthly_gross_wage_50_pctile",
    "mthly_basic_wage_50_pctile"
FROM "sg-data-d-670c3c6cecbcd24e48034a3428bd306e"
