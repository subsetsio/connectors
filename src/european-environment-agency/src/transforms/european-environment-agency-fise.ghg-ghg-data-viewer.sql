SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("gas" AS VARCHAR) AS "gas",
    CAST("notation" AS VARCHAR) AS "notation",
    CAST("sector_code" AS VARCHAR) AS "sector_code",
    CAST("sector_name" AS VARCHAR) AS "sector_name",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("value" AS VARCHAR) AS "value",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.ghg-ghg-data-viewer"
