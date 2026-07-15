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
    "4WorkingPersons" AS 4workingpersons,
    "5OrMoreWorkingPersons" AS 5ormoreworkingpersons
FROM "sg-data-d-f580f3689f8dc0e4686dc9e0a6a43de0"
