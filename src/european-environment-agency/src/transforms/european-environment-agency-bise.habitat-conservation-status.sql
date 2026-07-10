SELECT
    CAST("assessment_label" AS VARCHAR) AS "assessment_label",
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("id_assessment" AS VARCHAR) AS "id_assessment",
    CAST("region_name" AS VARCHAR) AS "region_name"
FROM "european-environment-agency-bise.habitat-conservation-status"
