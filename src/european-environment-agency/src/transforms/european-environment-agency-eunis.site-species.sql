SELECT
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("code_site" AS VARCHAR) AS "code_site",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("picture_url" AS VARCHAR) AS "picture_url",
    CAST("species_group_name" AS VARCHAR) AS "species_group_name",
    CAST("species_name" AS VARCHAR) AS "species_name"
FROM "european-environment-agency-eunis.site-species"
