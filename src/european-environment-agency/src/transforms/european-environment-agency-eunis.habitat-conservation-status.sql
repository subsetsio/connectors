SELECT
    CAST("conclusion_assessment" AS VARCHAR) AS "conclusion_assessment",
    CAST("conclusion_assessment_label" AS VARCHAR) AS "conclusion_assessment_label",
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("eunis_area_code" AS VARCHAR) AS "eunis_area_code",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("id_habitat" AS VARCHAR) AS "id_habitat",
    CAST("region_name" AS VARCHAR) AS "region_name"
FROM "european-environment-agency-eunis.habitat-conservation-status"
