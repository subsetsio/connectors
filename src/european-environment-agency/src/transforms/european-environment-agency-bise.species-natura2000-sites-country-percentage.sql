SELECT
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("percentage_sites" AS VARCHAR) AS "percentage_sites"
FROM "european-environment-agency-bise.species-natura2000-sites-country-percentage"
