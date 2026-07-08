SELECT
    CAST(snapshot_date AS DATE)      AS snapshot_date,
    namespace,
    repo,
    CAST(pull_count AS BIGINT)       AS pull_count,
    CAST(star_count AS BIGINT)       AS star_count,
    CAST(last_updated AS TIMESTAMP)  AS last_updated
FROM "docker-hub-pull-stats"
WHERE repo IS NOT NULL
  AND pull_count IS NOT NULL
