-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "make",
    "number"
FROM "sg-data-d-ab595ec8b7cbcb7a40d49e5435c2f78a"
