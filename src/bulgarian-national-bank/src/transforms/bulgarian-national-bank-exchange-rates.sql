SELECT
    CAST(date AS DATE)                       AS date,
    currency_code,
    currency_name,
    ratio,
    rate_bgn,
    reverse_rate,
    rate_bgn / NULLIF(ratio, 0)              AS rate_bgn_per_unit,
    currency_code IN ('XAU', 'XAG', 'XPT', 'XPD') AS is_metal
FROM (
    SELECT *, row_number() OVER (
        PARTITION BY date, currency_code ORDER BY rate_bgn
    ) AS rn
    FROM "bulgarian-national-bank-exchange-rates"
)
WHERE rn = 1 AND rate_bgn IS NOT NULL
