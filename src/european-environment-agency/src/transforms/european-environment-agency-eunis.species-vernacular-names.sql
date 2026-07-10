SELECT
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("id_dc" AS VARCHAR) AS "id_dc",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("language_code" AS VARCHAR) AS "language_code",
    CAST("language_name" AS VARCHAR) AS "language_name",
    CAST("source" AS VARCHAR) AS "source",
    CAST("vernacular_name" AS VARCHAR) AS "vernacular_name"
FROM "european-environment-agency-eunis.species-vernacular-names"
