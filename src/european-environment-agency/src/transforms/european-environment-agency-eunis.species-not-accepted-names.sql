SELECT
    CAST("author" AS VARCHAR) AS "author",
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("not_accepted_author" AS VARCHAR) AS "not_accepted_author",
    CAST("not_accepted_code_2000" AS VARCHAR) AS "not_accepted_code_2000",
    CAST("not_accepted_id_eunis" AS VARCHAR) AS "not_accepted_id_eunis",
    CAST("not_accepted_scientific_name" AS VARCHAR) AS "not_accepted_scientific_name",
    CAST("scientific_name" AS VARCHAR) AS "scientific_name",
    CAST("status_name" AS VARCHAR) AS "status_name"
FROM "european-environment-agency-eunis.species-not-accepted-names"
