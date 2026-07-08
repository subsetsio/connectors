SELECT
    TRY_CAST("date" AS DATE)                          AS date,
    "country_code"                                    AS country_code,
    "country"                                         AS country,
    TRY_CAST("pay_transparency_pct" AS DOUBLE)        AS pay_transparency_pct,
    TRY_CAST("pay_transparency_pct_3ma" AS DOUBLE)    AS pay_transparency_pct_3ma
FROM "indeed-hiring-lab-pay-transparency-country"
WHERE TRY_CAST("date" AS DATE) IS NOT NULL
