SELECT
    sheet,
    row_idx,
    period,
    CAST(period_date AS DATE) AS date,
    series,
    value,
    value_text
FROM "sf-fed-zero-lower-bound-probabilities-at-different-time-horizons"
WHERE value IS NOT NULL OR value_text IS NOT NULL
