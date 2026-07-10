SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("number_sites" AS VARCHAR) AS "number_sites"
FROM "european-environment-agency-bise.species-emerald-sites-country"
