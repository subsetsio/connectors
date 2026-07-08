SELECT
    SERCODIGO                              AS series_code,
    CAST(substr(VALDATA, 1, 10) AS DATE)   AS date,
    CAST(VALVALOR AS DOUBLE)               AS value,
    NULLIF(NIVNOME, '')                    AS geo_level,
    NULLIF(TERCODIGO, '')                  AS territory_code
FROM "ipea-values"
WHERE VALVALOR IS NOT NULL
  AND VALDATA IS NOT NULL
