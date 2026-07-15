-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NoEmployedPerson" AS noemployedperson,
    "1EmployedPerson" AS 1employedperson,
    "2EmployedPersons" AS 2employedpersons,
    "3EmployedPersons" AS 3employedpersons,
    "4EmployedPersons" AS 4employedpersons,
    "5orMoreEmployedPersons" AS 5ormoreemployedpersons
FROM "sg-data-d-6111e91466ff01ace4eaf7287d99a03f"
