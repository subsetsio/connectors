-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "15_24",
    "25_34",
    "35_44",
    "45_54",
    "55andOver" AS 55andover
FROM "sg-data-d-ed0b26013488649aafa52c4c5547ee5e"
