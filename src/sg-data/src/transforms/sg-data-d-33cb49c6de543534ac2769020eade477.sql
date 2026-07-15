-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "15_19Years" AS 15_19years,
    "20_24Years" AS 20_24years,
    "25_29Years" AS 25_29years,
    "30_34Years" AS 30_34years,
    "35_39Years" AS 35_39years,
    "40_44Years" AS 40_44years,
    "45_49Years" AS 45_49years,
    "50_54Years" AS 50_54years,
    "55YearsandOver" AS 55yearsandover
FROM "sg-data-d-33cb49c6de543534ac2769020eade477"
