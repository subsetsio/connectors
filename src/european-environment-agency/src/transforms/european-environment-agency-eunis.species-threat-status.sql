SELECT
    CAST("area_name_en" AS VARCHAR) AS "area_name_en",
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("eunis_area_code" AS VARCHAR) AS "eunis_area_code",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("threat_code" AS VARCHAR) AS "threat_code",
    CAST("threat_name" AS VARCHAR) AS "threat_name"
FROM "european-environment-agency-eunis.species-threat-status"
