-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "1Person" AS 1person,
    "2Persons" AS 2persons,
    "3Persons" AS 3persons,
    "4Persons" AS 4persons,
    "5Persons" AS 5persons,
    "6Persons" AS 6persons,
    "7Persons" AS 7persons,
    "8OrMorePersons" AS 8ormorepersons
FROM "sg-data-d-18488015a9d90903ba9d30f41bb24c6b"
