-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "industry1",
    "industry2",
    "highest_qualification_attained",
    "employed"
FROM "sg-data-d-1fb424886ad6498b8805e0b7299c4d6d"
