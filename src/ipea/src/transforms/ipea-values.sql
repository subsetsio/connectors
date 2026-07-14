SELECT DISTINCT
    SERCODIGO                              AS series_code,
    CAST(substr(VALDATA, 1, 10) AS DATE)   AS date,
    CAST(VALVALOR AS DOUBLE)               AS value,
    COALESCE(NULLIF(NIVNOME, ''), 'not_applicable') AS geo_level,
    COALESCE(NULLIF(TERCODIGO, ''), 'not_applicable') AS territory_code
FROM "ipea-values"
WHERE VALVALOR IS NOT NULL
  AND VALDATA IS NOT NULL
  -- IPEA uses 9999-01-01 for undated climate-normal series; exclude them from
  -- this temporal observations table so date freshness remains meaningful.
  AND substr(VALDATA, 1, 4) <> '9999'
