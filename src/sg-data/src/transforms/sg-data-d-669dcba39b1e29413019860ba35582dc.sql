-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "1Person" AS 1person,
    "2Persons" AS 2persons,
    "3Persons" AS 3persons,
    "4Persons" AS 4persons,
    "5Persons" AS 5persons,
    "6OrMorePersons" AS 6ormorepersons
FROM "sg-data-d-669dcba39b1e29413019860ba35582dc"
