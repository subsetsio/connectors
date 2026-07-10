SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("habitatcode" AS VARCHAR) AS "habitatcode",
    CAST("habitatname" AS VARCHAR) AS "habitatname",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("regions" AS VARCHAR) AS "regions"
FROM "european-environment-agency-fise.v-countryfact-n2k-art17-forest-habitats-per-country"
