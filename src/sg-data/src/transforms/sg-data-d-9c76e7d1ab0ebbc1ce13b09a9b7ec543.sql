-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "Below30Years" AS below30years,
    "30_34Years" AS 30_34years,
    "35_39Years" AS 35_39years,
    "40_44Years" AS 40_44years,
    "45_49Years" AS 45_49years,
    "50_54Years" AS 50_54years,
    "55_59Years" AS 55_59years,
    "60_64Years" AS 60_64years,
    "65_69Years" AS 65_69years,
    "70_74Years" AS 70_74years,
    "75YearsandOver" AS 75yearsandover
FROM "sg-data-d-9c76e7d1ab0ebbc1ce13b09a9b7ec543"
