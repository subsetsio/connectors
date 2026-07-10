SELECT
    CAST("id_dc" AS VARCHAR) AS "id_dc",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("language_name" AS VARCHAR) AS "language_name",
    CAST("source" AS VARCHAR) AS "source",
    CAST("vernacular_name" AS VARCHAR) AS "vernacular_name"
FROM "european-environment-agency-bise.species-vernacular-names"
