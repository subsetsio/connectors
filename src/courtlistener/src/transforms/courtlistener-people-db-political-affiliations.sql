SELECT
    TRY_CAST("id" AS BIGINT) AS "id",
    TRY_CAST("date_created" AS TIMESTAMP) AS "date_created",
    TRY_CAST("date_modified" AS TIMESTAMP) AS "date_modified",
    "political_party",
    "source",
    TRY_CAST("date_start" AS DATE) AS "date_start",
    "date_granularity_start",
    TRY_CAST("date_end" AS DATE) AS "date_end",
    "date_granularity_end",
    TRY_CAST("person_id" AS BIGINT) AS "person_id"
FROM "courtlistener-people-db-political-affiliations"
