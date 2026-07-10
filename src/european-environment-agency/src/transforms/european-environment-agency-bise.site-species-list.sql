SELECT
    CAST("common_name" AS VARCHAR) AS "common_name",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("scientific_name" AS VARCHAR) AS "scientific_name",
    CAST("site_code" AS VARCHAR) AS "site_code",
    CAST("species_group_name" AS VARCHAR) AS "species_group_name"
FROM "european-environment-agency-bise.site-species-list"
