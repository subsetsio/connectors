SELECT
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("id_site" AS VARCHAR) AS "id_site",
    CAST("site_name" AS VARCHAR) AS "site_name"
FROM "european-environment-agency-eunis.species-natura2000-sites"
