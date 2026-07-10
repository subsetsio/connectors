SELECT
    CAST("caves" AS VARCHAR) AS "caves",
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("coverage_ha" AS VARCHAR) AS "coverage_ha",
    CAST("habitat_description" AS VARCHAR) AS "habitat_description",
    CAST("habitat_group" AS VARCHAR) AS "habitat_group",
    CAST("priority" AS VARCHAR) AS "priority",
    CAST("priority_form_habitat_type" AS VARCHAR) AS "priority_form_habitat_type",
    CAST("site_code" AS VARCHAR) AS "site_code"
FROM "european-environment-agency-bise.site-habitats-list"
