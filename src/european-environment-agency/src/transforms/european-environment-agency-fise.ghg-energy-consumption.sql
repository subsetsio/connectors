SELECT
    CAST("category" AS VARCHAR) AS "category",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("data_source" AS VARCHAR) AS "data_source",
    CAST("extracted_on" AS VARCHAR) AS "extracted_on",
    CAST("id" AS VARCHAR) AS "id",
    CAST("ImportRecordId" AS VARCHAR) AS "ImportRecordId",
    CAST("indic_nrg" AS VARCHAR) AS "indic_nrg",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("value" AS VARCHAR) AS "value",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.ghg-energy-consumption"
