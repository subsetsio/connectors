SELECT
    CAST("assessment" AS VARCHAR) AS "assessment",
    CAST("assessment_order" AS VARCHAR) AS "assessment_order",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("habitat_group" AS VARCHAR) AS "habitat_group",
    CAST("quantity" AS VARCHAR) AS "quantity"
FROM "european-environment-agency-bise.country-conservation-status-habitats-by-habitat-group"
