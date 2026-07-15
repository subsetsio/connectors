-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "policyholders",
    "policyholders_with_supplements"
FROM "sg-data-d-6df6086af759a419ea8140f4b057eb0d"
