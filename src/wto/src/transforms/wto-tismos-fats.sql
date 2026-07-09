SELECT
    FLOW                        AS flow,
    REPORTER                    AS reporter,
    PARTNER                     AS partner,
    INDICATOR                   AS indicator,
    TRY_CAST(YEAR AS INTEGER)   AS year,
    TRY_CAST(VALUE AS DOUBLE)   AS value,
    NULLIF(METH, '')            AS method
FROM "wto-tismos-fats"
WHERE TRY_CAST(YEAR AS INTEGER) IS NOT NULL
  AND TRY_CAST(VALUE AS DOUBLE) IS NOT NULL
