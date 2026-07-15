-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "rank",
    "icd",
    "classification",
    "disease_condition",
    "percentage_deaths"
FROM "sg-data-d-48143a2b16027afcadeb362352b0266a"
