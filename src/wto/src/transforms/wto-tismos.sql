SELECT
    FLOW                        AS flow,
    REPORTER                    AS reporter,
    PARTNER                     AS partner,
    INDICATOR                   AS indicator,
    TRY_CAST(YEAR AS INTEGER)   AS year,
    MODE                        AS mode_of_supply,
    TRY_CAST(VALUE AS DOUBLE)   AS value,
    METH                        AS method
FROM "wto-tismos"
WHERE TRY_CAST(YEAR AS INTEGER) IS NOT NULL
  AND TRY_CAST(VALUE AS DOUBLE) IS NOT NULL
