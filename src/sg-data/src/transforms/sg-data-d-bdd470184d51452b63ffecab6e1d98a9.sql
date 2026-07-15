-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Incidence_Rate" AS incidence_rate
FROM "sg-data-d-bdd470184d51452b63ffecab6e1d98a9"
