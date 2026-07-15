-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "company",
    "taxi_fleet"
FROM "sg-data-d-884c2efb2103bc66dc2b8725173be85b"
