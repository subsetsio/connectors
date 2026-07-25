SELECT
    SERCODIGO                              AS series_code,
    CASE
        WHEN substr(VALDATA, 1, 10) = '9999-01-01' THEN NULL
        ELSE CAST(substr(VALDATA, 1, 10) AS DATE)
    END                                    AS date,
    substr(VALDATA, 1, 10) = '9999-01-01' AS has_unknown_date,
    CAST(VALVALOR AS DOUBLE)               AS value,
    COALESCE(NULLIF(NIVNOME, ''), 'not_applicable') AS geo_level,
    COALESCE(NULLIF(TERCODIGO, ''), 'not_applicable') AS territory_code
FROM "ipea-values"
