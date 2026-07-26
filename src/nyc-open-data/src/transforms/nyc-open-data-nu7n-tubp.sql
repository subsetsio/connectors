-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "animalname",
    "animalgender",
    "animalbirthyear",
    "breedname",
    CAST("zipcode" AS BIGINT) AS zipcode,
    strptime("licenseissueddate", '%m/%d/%Y')::DATE AS licenseissueddate,
    strptime("licenseexpireddate", '%m/%d/%Y')::DATE AS licenseexpireddate,
    CAST("extract_year" AS BIGINT) AS extract_year
FROM "nyc-open-data-nu7n-tubp"
