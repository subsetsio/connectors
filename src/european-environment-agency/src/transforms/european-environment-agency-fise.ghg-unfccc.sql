SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("emissions" AS VARCHAR) AS "emissions",
    CAST("Format_name" AS VARCHAR) AS "Format_name",
    CAST("id" AS VARCHAR) AS "id",
    CAST("ImportRecordId" AS VARCHAR) AS "ImportRecordId",
    CAST("Notation" AS VARCHAR) AS "Notation",
    CAST("parent_sector_code_id" AS VARCHAR) AS "parent_sector_code_id",
    CAST("Pollutant_name" AS VARCHAR) AS "Pollutant_name",
    CAST("sector_code_id" AS VARCHAR) AS "sector_code_id",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.ghg-unfccc"
