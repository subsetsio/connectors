WITH cleaned AS (
    SELECT
        TRY_CAST(series_id AS BIGINT) AS series_id,
        series_code,
        series_name,
        units,
        entity_id,
        entity_iso,
        entity_name,
        data_year AS year,
        TRY_CAST(data_value AS DOUBLE) AS value,
        data_value AS value_raw,
        data_note,
        data_source,
        requested_code_id
    FROM "itu-values"
    WHERE data_value IS NOT NULL
      AND data_value <> ''
      AND data_year IS NOT NULL
      AND entity_iso IS NOT NULL
),
ranked AS (
    SELECT *,
        row_number() OVER (
            PARTITION BY series_id, entity_iso, year
            ORDER BY requested_code_id
        ) AS rn
    FROM cleaned
)
SELECT
    series_id,
    series_code,
    series_name,
    units,
    entity_id,
    entity_iso,
    entity_name,
    year,
    value,
    value_raw,
    data_note,
    data_source
FROM ranked
WHERE rn = 1
