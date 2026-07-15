-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Incidence_Rate" AS incidence_rate
FROM "sg-data-d-3a6a142859398cd6b14f8a071b8f4cf3"
