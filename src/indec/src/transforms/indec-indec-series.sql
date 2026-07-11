SELECT DISTINCT
    series_id,
    title,
    description,
    frequency,
    units,
    CAST(time_index_start AS DATE) AS time_index_start,
    CAST(time_index_end   AS DATE) AS time_index_end,
    dataset_title,
    dataset_source,
    dataset_theme,
    dataset_publisher
FROM "indec-indec-series"
WHERE series_id IS NOT NULL
