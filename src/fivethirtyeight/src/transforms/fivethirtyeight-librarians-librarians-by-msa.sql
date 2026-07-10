-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "prim_state",
    "area_name",
    "tot_emp",
    "emp_prse",
    "jobs_1000",
    "loc_quotient"
FROM "fivethirtyeight-librarians-librarians-by-msa"
