SELECT
    CAST(observation_date AS DATE) AS observation_date,
    CAST(doc_count AS BIGINT)      AS doc_count,
    CAST(update_seq AS BIGINT)     AS update_seq
FROM "npm-registry-stats"
WHERE observation_date IS NOT NULL
