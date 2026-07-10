SELECT
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("level" AS VARCHAR) AS "level",
    CAST("level_name" AS VARCHAR) AS "level_name",
    CAST("scientific_name" AS VARCHAR) AS "scientific_name"
FROM "european-environment-agency-bise.species-taxonomy"
