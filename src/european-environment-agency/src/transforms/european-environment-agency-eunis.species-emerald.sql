SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("id_site" AS VARCHAR) AS "id_site",
    CAST("id_species" AS VARCHAR) AS "id_species",
    CAST("id_species_name" AS VARCHAR) AS "id_species_name",
    CAST("site_name" AS VARCHAR) AS "site_name",
    CAST("species_code" AS VARCHAR) AS "species_code"
FROM "european-environment-agency-eunis.species-emerald"
