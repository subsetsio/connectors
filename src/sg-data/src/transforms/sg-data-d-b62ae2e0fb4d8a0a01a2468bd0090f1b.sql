-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "median_dur_of_unemp"
FROM "sg-data-d-b62ae2e0fb4d8a0a01a2468bd0090f1b"
