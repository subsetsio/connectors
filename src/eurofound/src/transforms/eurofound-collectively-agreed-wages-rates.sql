SELECT
    country,
    CAST(year AS INTEGER)                                       AS year,
    month,
    CAST(try_strptime(NULLIF(month, '') || ' ' || CAST(year AS VARCHAR), '%B %Y') AS DATE) AS period,
    sector,
    wage_type,
    frequency,
    series,
    series_title,
    agreement_id,
    TRY_CAST(value AS DOUBLE)            AS value,
    TRY_CAST(rate_eur AS DOUBLE)         AS rate_eur,
    TRY_CAST(rate_national AS DOUBLE)    AS rate_national,
    TRY_CAST(rate_eur_month AS DOUBLE)   AS rate_eur_month,
    TRY_CAST(rate_nat_month AS DOUBLE)   AS rate_nat_month,
    TRY_CAST(working_hours AS DOUBLE)    AS working_hours,
    TRY_CAST(annual_payments AS DOUBLE)  AS annual_payments
FROM "eurofound-collectively-agreed-wages-rates"
WHERE country IS NOT NULL AND year IS NOT NULL
