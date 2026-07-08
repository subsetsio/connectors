SELECT
    CAST(appid AS BIGINT)           AS appid,
    CAST(review_score AS INTEGER)   AS review_score,
    review_score_desc,
    CAST(total_positive AS BIGINT)  AS total_positive,
    CAST(total_negative AS BIGINT)  AS total_negative,
    CAST(total_reviews AS BIGINT)   AS total_reviews
FROM "steamdb-app-reviews"
WHERE appid IS NOT NULL
