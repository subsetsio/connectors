SELECT
    CAST("conservation_of_biodiversity" AS VARCHAR) AS "conservation_of_biodiversity",
    CAST("country" AS VARCHAR) AS "country",
    CAST("multiple_use" AS VARCHAR) AS "multiple_use",
    CAST("no_unknown" AS VARCHAR) AS "no_unknown",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("other" AS VARCHAR) AS "other",
    CAST("production" AS VARCHAR) AS "production",
    CAST("protection_of_soil_and_water" AS VARCHAR) AS "protection_of_soil_and_water",
    CAST("social_services" AS VARCHAR) AS "social_services",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-management-soef20-primary-designated-management-objective"
