SELECT
    project_slug,
    CAST(to_timestamp(timestamp) AS DATE) AS date,
    native,
    canonical,
    external,
    COALESCE(native, 0) + COALESCE(canonical, 0) + COALESCE(external, 0) AS total_usd,
    eth_price
FROM "l2beat-tvs"
WHERE timestamp IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY project_slug, CAST(to_timestamp(timestamp) AS DATE)
    ORDER BY timestamp DESC
) = 1
