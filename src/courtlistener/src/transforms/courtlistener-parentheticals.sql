SELECT
    TRY_CAST("id" AS BIGINT) AS "id",
    "text",
    TRY_CAST("score" AS DOUBLE) AS "score",
    TRY_CAST("described_opinion_id" AS BIGINT) AS "described_opinion_id",
    TRY_CAST("describing_opinion_id" AS BIGINT) AS "describing_opinion_id",
    TRY_CAST("group_id" AS BIGINT) AS "group_id"
FROM "courtlistener-parentheticals"
