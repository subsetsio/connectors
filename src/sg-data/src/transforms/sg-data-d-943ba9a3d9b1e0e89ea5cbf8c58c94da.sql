-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "graduate_type",
    "no_of_graduates"
FROM "sg-data-d-943ba9a3d9b1e0e89ea5cbf8c58c94da"
