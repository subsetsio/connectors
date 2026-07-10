SELECT
    CAST("area_name_en" AS VARCHAR) AS "area_name_en",
    CAST("assessment_label" AS VARCHAR) AS "assessment_label",
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("id_assessment" AS VARCHAR) AS "id_assessment",
    CAST("region_name" AS VARCHAR) AS "region_name"
FROM "european-environment-agency-bise.habitat-conservation-status-by-ms"
