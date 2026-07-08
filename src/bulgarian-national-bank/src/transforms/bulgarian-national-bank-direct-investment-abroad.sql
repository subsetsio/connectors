SELECT
    keyfamily,
    freq,
    series_key,
    series_name,
    period,
    value
FROM (
    SELECT *, row_number() OVER (
        PARTITION BY series_key, freq, period ORDER BY value
    ) AS rn
    FROM "bulgarian-national-bank-direct-investment-abroad"
)
WHERE rn = 1 AND value IS NOT NULL
