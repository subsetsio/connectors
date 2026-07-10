SELECT
    CAST("assessment" AS VARCHAR) AS "assessment",
    CAST("assessment_order" AS VARCHAR) AS "assessment_order",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("habitats_assessment" AS VARCHAR) AS "habitats_assessment",
    CAST("percentage_assessment" AS VARCHAR) AS "percentage_assessment",
    CAST("total_species" AS VARCHAR) AS "total_species"
FROM "european-environment-agency-bise.country-conservation-status-habitats-habitats-directive"
