SELECT
    CAST("caves" AS VARCHAR) AS "caves",
    CAST("code_site" AS VARCHAR) AS "code_site",
    CAST("cover_ha" AS VARCHAR) AS "cover_ha",
    CAST("habitat_code" AS VARCHAR) AS "habitat_code",
    CAST("habitat_name" AS VARCHAR) AS "habitat_name",
    CAST("priority" AS VARCHAR) AS "priority",
    CAST("priority_form_habitat_type" AS VARCHAR) AS "priority_form_habitat_type"
FROM "european-environment-agency-eunis.site-habitat-type"
