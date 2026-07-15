-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "level_of_school",
    "length_of_service",
    "no_of_principals"
FROM "sg-data-d-c1295bd1935f06ac0646a10efbf07dbf"
