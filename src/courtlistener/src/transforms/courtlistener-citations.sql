SELECT
    TRY_CAST("id" AS BIGINT) AS "id",
    "volume",
    "reporter",
    "page",
    "type",
    TRY_CAST("cluster_id" AS BIGINT) AS "cluster_id",
    TRY_CAST("date_created" AS TIMESTAMP) AS "date_created",
    TRY_CAST("date_modified" AS TIMESTAMP) AS "date_modified"
FROM "courtlistener-citations"
