-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "occupation",
    "highest_qualification_attained",
    "employed"
FROM "sg-data-d-576bb1f46eabb041d8d966030170ec6f"
