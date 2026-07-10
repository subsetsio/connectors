SELECT
    CAST("area_code" AS VARCHAR) AS "area_code",
    CAST("area_name_en" AS VARCHAR) AS "area_name_en",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("id_habitat" AS VARCHAR) AS "id_habitat",
    CAST("id_site" AS VARCHAR) AS "id_site",
    CAST("name" AS VARCHAR) AS "name"
FROM "european-environment-agency-eunis.habitat-emerald"
