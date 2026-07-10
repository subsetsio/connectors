SELECT
    CAST("Country_name" AS VARCHAR) AS "Country_name",
    CAST("EEA38" AS VARCHAR) AS "EEA38",
    CAST("EEA39" AS VARCHAR) AS "EEA39",
    CAST("EU27" AS VARCHAR) AS "EU27",
    CAST("EU28" AS VARCHAR) AS "EU28",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("Units" AS VARCHAR) AS "Units",
    CAST("volume" AS VARCHAR) AS "volume",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-countryfact-inforest-general-growing-stock"
