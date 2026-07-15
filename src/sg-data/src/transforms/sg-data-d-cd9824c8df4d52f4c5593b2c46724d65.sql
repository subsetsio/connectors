-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NoWorkingPerson" AS noworkingperson,
    "1WorkingPerson" AS 1workingperson,
    "2WorkingPersons" AS 2workingpersons,
    "3WorkingPersons" AS 3workingpersons,
    "4OrMoreWorkingPersons" AS 4ormoreworkingpersons
FROM "sg-data-d-cd9824c8df4d52f4c5593b2c46724d65"
