SELECT
    series_id,
    source,
    short_description,
    mid_description,
    long_description,
    group_id,
    CAST(observation_min_date AS DATE) AS observation_min_date,
    CAST(observation_max_date AS DATE) AS observation_max_date,
    series_closed
FROM "sveriges-riksbank-series"
WHERE series_id IS NOT NULL
