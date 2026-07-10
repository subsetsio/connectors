SELECT
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("synonym_author" AS VARCHAR) AS "synonym_author",
    CAST("synonym_id_eunis" AS VARCHAR) AS "synonym_id_eunis",
    CAST("synonym_scientific_name" AS VARCHAR) AS "synonym_scientific_name"
FROM "european-environment-agency-bise.species-synonym-names"
