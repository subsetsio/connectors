SELECT
    period_label,
    CASE WHEN period_ms IS NOT NULL
         THEN epoch_ms(CAST(period_ms AS BIGINT)) END AS period_ts,
    series,
    CAST(value AS DOUBLE)                            AS value
FROM "eskom-monthly-generation-capacity-breakdown"
WHERE value IS NOT NULL
  AND period_label IS NOT NULL
  AND series IS NOT NULL
