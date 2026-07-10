SELECT
    CAST(round_num AS INTEGER) AS round_num,
    CAST(round_id AS BIGINT) AS round_id,
    round_label,
    CAST(start_year AS INTEGER) AS start_year,
    CAST(end_year AS INTEGER) AS end_year
FROM "afrobarometer-rounds"
WHERE round_num IS NOT NULL
