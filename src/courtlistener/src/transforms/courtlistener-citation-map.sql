SELECT
    TRY_CAST("id" AS BIGINT) AS "id",
    TRY_CAST("depth" AS BIGINT) AS "depth",
    TRY_CAST("cited_opinion_id" AS BIGINT) AS "cited_opinion_id",
    TRY_CAST("citing_opinion_id" AS BIGINT) AS "citing_opinion_id"
FROM "courtlistener-citation-map"
