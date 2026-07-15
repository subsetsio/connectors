-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "waste_disposed_of",
    "waste_recycled"
FROM "sg-data-d-96d95bfc9867daa138a451950dc7cc4e"
