-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "didnotparticipatepastyear",
    "inactive",
    "irregular",
    "regular"
FROM "sg-data-d-b70cb83dddceaee4d2256ffb6512f75a"
