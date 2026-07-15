-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "employment_size",
    "broadband_usage"
FROM "sg-data-d-29d9931cd926c398728a0654537c5d6e"
