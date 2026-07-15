-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nature_of_disputes",
    "number_of_disputes"
FROM "sg-data-d-c45e8a5f0fd6e51e83cfb6105dc2e1bd"
