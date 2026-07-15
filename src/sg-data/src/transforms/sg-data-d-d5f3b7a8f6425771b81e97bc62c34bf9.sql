-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "didnotparticipatepastyear",
    "inactive",
    "irregular",
    "regular"
FROM "sg-data-d-d5f3b7a8f6425771b81e97bc62c34bf9"
