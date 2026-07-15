-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "admissions_by_gender",
    "number_of_admissions"
FROM "sg-data-d-20ec1aef68ae8f3510013752a33e7a89"
