WITH ranked AS (
    SELECT
        CAST(obs_date AS DATE)                       AS date,
        TRY_CAST(dimension_date AS DATE)             AS dimension_date,
        series_id,
        series_title,
        description,
        frequency,
        series_type                                  AS type,
        units,
        source,
        partition_key,
        TRY_CAST(value_text AS DOUBLE)               AS value,
        value_text,
        row_number() OVER (
            PARTITION BY series_id, obs_date, dimension_date, partition_key
            ORDER BY COALESCE(
                TRY_STRPTIME(publication_date, '%d-%b-%Y'),
                TRY_STRPTIME(publication_date, '%d-%b-%y')
            ) DESC NULLS LAST
        ) AS rn
    FROM "reserve-bank-of-australia-d1-data"
    WHERE value_text IS NOT NULL AND value_text <> ''
      AND series_id IS NOT NULL
      AND TRY_CAST(obs_date AS DATE) IS NOT NULL
)
SELECT date, dimension_date, series_id, series_title, description,
       frequency, type, units, source, partition_key, value, value_text
FROM ranked
WHERE rn = 1
