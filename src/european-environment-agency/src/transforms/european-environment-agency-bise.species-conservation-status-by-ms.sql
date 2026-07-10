SELECT
    CAST("area_name_en" AS VARCHAR) AS "area_name_en",
    CAST("assessment_label" AS VARCHAR) AS "assessment_label",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("id_assessment" AS VARCHAR) AS "id_assessment",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("region_name" AS VARCHAR) AS "region_name"
FROM "european-environment-agency-bise.species-conservation-status-by-ms"
