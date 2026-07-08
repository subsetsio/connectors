SELECT
    CAST(year AS INTEGER)        AS year,
    state                        AS state,
    TRY_CAST(gallons AS BIGINT)  AS gallons_taxed
FROM "fhwa-hvfw-tcmn"
WHERE year IS NOT NULL AND state IS NOT NULL
  AND TRY_CAST(year AS INTEGER) IS NOT NULL
