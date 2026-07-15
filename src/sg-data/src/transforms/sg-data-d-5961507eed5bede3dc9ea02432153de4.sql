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
    "percentage_discharges"
FROM "sg-data-d-5961507eed5bede3dc9ea02432153de4"
