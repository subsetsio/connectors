-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "occ_desc",
    "mthly_gross_wage_75_pctile",
    "mthly_gross_wage_50_pctile",
    "mthly_gross_wage_25_pctile",
    "mthly_basic_wage_75_pctile",
    "mthly_basic_wage_50_pctile",
    "mthly_basic_wage_25_pctile"
FROM "sg-data-d-9917e751f7498502f70052a940a3f312"
