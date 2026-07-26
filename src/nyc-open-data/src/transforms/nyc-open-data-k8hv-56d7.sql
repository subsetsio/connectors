-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "demographic",
    "dbn",
    "_name" AS name,
    "total_cohort_june",
    "total_mathela_apm_june",
    "of_cohort_june",
    "total_cohort_august",
    "total_mathela_apm_august",
    "of_cohort_august"
FROM "nyc-open-data-k8hv-56d7"
