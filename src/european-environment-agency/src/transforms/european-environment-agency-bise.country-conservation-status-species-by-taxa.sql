SELECT
    CAST("assessment" AS VARCHAR) AS "assessment",
    CAST("assessment_order" AS VARCHAR) AS "assessment_order",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("quantity" AS VARCHAR) AS "quantity",
    CAST("species_group" AS VARCHAR) AS "species_group"
FROM "european-environment-agency-bise.country-conservation-status-species-by-taxa"
