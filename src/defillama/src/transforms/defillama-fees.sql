SELECT
    CAST(protocol_id AS VARCHAR)  AS protocol_id,
    name,
    display_name,
    slug,
    category,
    protocol_type,
    chains,
    CAST(total_24h AS DOUBLE)     AS total_24h,
    CAST(total_7d AS DOUBLE)      AS total_7d,
    CAST(total_30d AS DOUBLE)     AS total_30d,
    CAST(total_1y AS DOUBLE)      AS total_1y,
    CAST(total_all_time AS DOUBLE) AS total_all_time,
    CAST(average_1y AS DOUBLE)    AS average_1y,
    CAST(change_1d AS DOUBLE)     AS change_1d,
    CAST(change_7d AS DOUBLE)     AS change_7d,
    CAST(change_1m AS DOUBLE)     AS change_1m
FROM "defillama-fees"
WHERE name IS NOT NULL
