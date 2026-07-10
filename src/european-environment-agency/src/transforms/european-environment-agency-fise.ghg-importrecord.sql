SELECT
    CAST("dataset" AS VARCHAR) AS "dataset",
    CAST("filename" AS VARCHAR) AS "filename",
    CAST("id" AS VARCHAR) AS "id",
    CAST("importDate" AS VARCHAR) AS "importDate",
    CAST("releaseDate" AS VARCHAR) AS "releaseDate",
    CAST("source" AS VARCHAR) AS "source"
FROM "european-environment-agency-fise.ghg-importrecord"
