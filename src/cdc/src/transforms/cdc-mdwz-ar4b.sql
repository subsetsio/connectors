-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Antifungal Class" AS antifungal_class,
    "Drug" AS drug,
    CAST("Year" AS BIGINT) AS year,
    "State Abbreviation" AS state_abbreviation,
    CAST("Number of Isolates" AS BIGINT) AS number_of_isolates,
    CAST("Number of Resistant Isolates" AS BIGINT) AS number_of_resistant_isolates,
    CAST("Percent Resistant" AS DOUBLE) AS percent_resistant,
    "Region" AS region,
    CAST("classID" AS BIGINT) AS classid,
    CAST("drugID" AS BIGINT) AS drugid,
    CAST("eventYearID" AS BIGINT) AS eventyearid,
    CAST("geographyID" AS BIGINT) AS geographyid
FROM "cdc-mdwz-ar4b"
