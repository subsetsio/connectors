-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "vaccination_type",
    "no_of_doses_in_thousands"
FROM "sg-data-d-5803ad431c25d4615416159a39858c7b"
