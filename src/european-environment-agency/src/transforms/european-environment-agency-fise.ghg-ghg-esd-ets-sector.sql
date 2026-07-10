SELECT
    CAST("category" AS VARCHAR) AS "category",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("gas" AS VARCHAR) AS "gas",
    CAST("id" AS VARCHAR) AS "id",
    CAST("ImportRecordId" AS VARCHAR) AS "ImportRecordId",
    CAST("scenario" AS VARCHAR) AS "scenario",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("value" AS VARCHAR) AS "value",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.ghg-ghg-esd-ets-sector"
