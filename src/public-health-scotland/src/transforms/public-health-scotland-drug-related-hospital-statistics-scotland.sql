-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "FinancialYear" AS financialyear,
    "HBR" AS hbr,
    "HBRQF" AS hbrqf,
    CAST("NumberOfStays" AS BIGINT) AS numberofstays,
    CAST("EASRStays" AS DOUBLE) AS easrstays,
    "CA" AS ca,
    "CAQF" AS caqf
FROM "public-health-scotland-drug-related-hospital-statistics-scotland"
