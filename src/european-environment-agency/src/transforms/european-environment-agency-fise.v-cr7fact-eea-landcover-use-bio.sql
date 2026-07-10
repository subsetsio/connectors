SELECT
    CAST("area" AS VARCHAR) AS "area",
    CAST("bio_code" AS VARCHAR) AS "bio_code",
    CAST("land_use_class" AS VARCHAR) AS "land_use_class",
    CAST("percentage" AS VARCHAR) AS "percentage",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-cr7fact-eea-landcover-use-bio"
