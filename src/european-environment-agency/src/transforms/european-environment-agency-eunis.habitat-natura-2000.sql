SELECT
    CAST("area_name_en" AS VARCHAR) AS "area_name_en",
    CAST("eunis_area_code" AS VARCHAR) AS "eunis_area_code",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("id_habitat" AS VARCHAR) AS "id_habitat",
    CAST("id_site" AS VARCHAR) AS "id_site",
    CAST("site_name" AS VARCHAR) AS "site_name"
FROM "european-environment-agency-eunis.habitat-natura-2000"
