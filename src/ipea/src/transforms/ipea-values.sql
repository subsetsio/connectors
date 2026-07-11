SELECT
    SERCODIGO                              AS series_code,
    CAST(substr(VALDATA, 1, 10) AS DATE)   AS date,
    CAST(VALVALOR AS DOUBLE)               AS value,
    COALESCE(NULLIF(NIVNOME, ''), 'not_applicable') AS geo_level,
    COALESCE(NULLIF(TERCODIGO, ''), 'not_applicable') AS territory_code
FROM "ipea-values"
WHERE VALVALOR IS NOT NULL
  AND VALDATA IS NOT NULL
