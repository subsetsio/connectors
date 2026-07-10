SELECT
    CAST("author_name" AS VARCHAR) AS "author_name",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("id_habitat" AS VARCHAR) AS "id_habitat",
    CAST("source" AS VARCHAR) AS "source",
    CAST("WebURL" AS VARCHAR) AS "WebURL"
FROM "european-environment-agency-eunis.habitat-redlist-photos"
