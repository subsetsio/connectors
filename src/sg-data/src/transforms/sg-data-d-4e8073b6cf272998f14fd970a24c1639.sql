-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "development_status",
    "no_of_units"
FROM "sg-data-d-4e8073b6cf272998f14fd970a24c1639"
