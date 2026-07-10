SELECT
    CAST("afforestation" AS VARCHAR) AS "afforestation",
    CAST("country" AS VARCHAR) AS "country",
    CAST("deforestation" AS VARCHAR) AS "deforestation",
    CAST("EEA38" AS VARCHAR) AS "EEA38",
    CAST("EEA39" AS VARCHAR) AS "EEA39",
    CAST("EU27" AS VARCHAR) AS "EU27",
    CAST("EU28" AS VARCHAR) AS "EU28",
    CAST("forest_expansion" AS VARCHAR) AS "forest_expansion",
    CAST("natural_expansion" AS VARCHAR) AS "natural_expansion",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-vita-gfra-forest-area-change"
