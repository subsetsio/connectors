SELECT
    CAST(year AS INTEGER)        AS year,
    state                        AS state,
    revenues                     AS revenue_source,
    TRY_CAST(dollars AS BIGINT)  AS dollars
FROM "fhwa-ix2d-bsqq"
WHERE year IS NOT NULL AND state IS NOT NULL AND revenues IS NOT NULL
  AND TRY_CAST(year AS INTEGER) IS NOT NULL
