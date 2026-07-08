SELECT
    iso3,
    country,
    CAST(year AS INTEGER) AS year,
    indicator_id,
    CAST(raw_value AS DOUBLE)   AS raw_value,
    CAST(input_value AS DOUBLE) AS input_value,
    CAST(score_value AS DOUBLE) AS score_value
FROM "nd-gain-indicators"
WHERE raw_value IS NOT NULL
   OR input_value IS NOT NULL
   OR score_value IS NOT NULL
