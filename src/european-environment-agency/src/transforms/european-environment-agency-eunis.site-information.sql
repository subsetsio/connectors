SELECT
    CAST("admin_region" AS VARCHAR) AS "admin_region",
    CAST("area_ha" AS VARCHAR) AS "area_ha",
    CAST("area_km2" AS VARCHAR) AS "area_km2",
    CAST("code_site" AS VARCHAR) AS "code_site",
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("eunis_area_code" AS VARCHAR) AS "eunis_area_code",
    CAST("marine_percent" AS VARCHAR) AS "marine_percent",
    CAST("national_code" AS VARCHAR) AS "national_code",
    CAST("natura_2000" AS VARCHAR) AS "natura_2000",
    CAST("nuts" AS VARCHAR) AS "nuts",
    CAST("site_name" AS VARCHAR) AS "site_name",
    CAST("site_type" AS VARCHAR) AS "site_type",
    CAST("source_db" AS VARCHAR) AS "source_db",
    CAST("spa_date" AS VARCHAR) AS "spa_date"
FROM "european-environment-agency-eunis.site-information"
