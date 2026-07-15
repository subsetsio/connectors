-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Incidence_Rate" AS incidence_rate
FROM "sg-data-d-71daf4b9690a30c37fa343bfe316d9f1"
