SELECT
    TRY_CAST(asOfDate AS DATE)           AS as_of_date,
    instrumentGroup                      AS instrument_group,
    securityType                         AS security_type,
    cusip,
    TRY_CAST(maturityDate AS DATE)       AS maturity_date,
    NULLIF(issuer, '')                   AS issuer,
    TRY_CAST(NULLIF(coupon, '') AS DOUBLE)   AS coupon_rate,
    TRY_CAST(NULLIF(parValue, '') AS DOUBLE) AS par_value,
    TRY_CAST(NULLIF(inflationCompensation, '') AS DOUBLE) AS inflation_compensation,
    TRY_CAST(NULLIF(percentOutstanding, '') AS DOUBLE)    AS percent_outstanding,
    TRY_CAST(NULLIF(changeFromPriorWeek, '') AS DOUBLE)   AS change_from_prior_week,
    TRY_CAST(NULLIF(changeFromPriorYear, '') AS DOUBLE)   AS change_from_prior_year
FROM "ny-fed-soma-holdings"
WHERE TRY_CAST(asOfDate AS DATE) IS NOT NULL AND cusip IS NOT NULL AND cusip <> ''
