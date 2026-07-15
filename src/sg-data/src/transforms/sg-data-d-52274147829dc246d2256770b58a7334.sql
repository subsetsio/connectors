-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "occupation",
    "resignation_rate"
FROM "sg-data-d-52274147829dc246d2256770b58a7334"
