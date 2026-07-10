SELECT
    CAST("gas" AS VARCHAR) AS "gas",
    CAST("notation" AS VARCHAR) AS "notation",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("sector_code" AS VARCHAR) AS "sector_code",
    CAST("sector_name" AS VARCHAR) AS "sector_name",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("value" AS VARCHAR) AS "value",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-clim-ghg-data-viewer"
