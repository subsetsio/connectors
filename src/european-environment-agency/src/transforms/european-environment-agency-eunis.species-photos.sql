SELECT
    CAST("attribution_copyright" AS VARCHAR) AS "attribution_copyright",
    CAST("author_name" AS VARCHAR) AS "author_name",
    CAST("eunis_id" AS VARCHAR) AS "eunis_id",
    CAST("filename" AS VARCHAR) AS "filename",
    CAST("filename_newName" AS VARCHAR) AS "filename_newName",
    CAST("id_photo" AS VARCHAR) AS "id_photo",
    CAST("id_species" AS VARCHAR) AS "id_species",
    CAST("main" AS VARCHAR) AS "main",
    CAST("Natura2000_code" AS VARCHAR) AS "Natura2000_code",
    CAST("scientific_name" AS VARCHAR) AS "scientific_name",
    CAST("sort_order" AS VARCHAR) AS "sort_order",
    CAST("ThumbnailURL" AS VARCHAR) AS "ThumbnailURL",
    CAST("WebURL" AS VARCHAR) AS "WebURL"
FROM "european-environment-agency-eunis.species-photos"
