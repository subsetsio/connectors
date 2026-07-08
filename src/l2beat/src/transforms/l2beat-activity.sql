SELECT
    project_slug,
    CAST(to_timestamp(timestamp) AS DATE) AS date,
    tx_count,
    uops_count
FROM "l2beat-activity"
WHERE timestamp IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY project_slug, CAST(to_timestamp(timestamp) AS DATE)
    ORDER BY timestamp DESC
) = 1
