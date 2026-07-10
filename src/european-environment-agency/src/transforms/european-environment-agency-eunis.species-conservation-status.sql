SELECT
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("conclusion_assessment" AS VARCHAR) AS "conclusion_assessment",
    CAST("conclusion_assessment_label" AS VARCHAR) AS "conclusion_assessment_label",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("region_name" AS VARCHAR) AS "region_name"
FROM "european-environment-agency-eunis.species-conservation-status"
