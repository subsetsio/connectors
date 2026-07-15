-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "town",
    "flat_type",
    "median_rent"
FROM "sg-data-d-23000a00c52996c55106084ed0339566"
