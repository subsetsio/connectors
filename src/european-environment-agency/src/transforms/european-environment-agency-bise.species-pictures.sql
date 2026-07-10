SELECT
    CAST("description" AS VARCHAR) AS "description",
    CAST("file_name" AS VARCHAR) AS "file_name",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("license" AS VARCHAR) AS "license",
    CAST("picture_url" AS VARCHAR) AS "picture_url",
    CAST("source" AS VARCHAR) AS "source",
    CAST("source_url" AS VARCHAR) AS "source_url"
FROM "european-environment-agency-bise.species-pictures"
