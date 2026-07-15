-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "flat_type",
    "no_of_resale_applications"
FROM "sg-data-d-02aa4bb51bc674f3a2d0b9bb6911d934"
