SELECT
    CAST("coverage_percentage" AS VARCHAR) AS "coverage_percentage",
    CAST("habitat_group" AS VARCHAR) AS "habitat_group",
    CAST("site_code" AS VARCHAR) AS "site_code"
FROM "european-environment-agency-bise.site-habitats-grouped-coverage-area-percentage"
