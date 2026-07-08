SELECT
    CAST(strptime(trim(release_date), '%m/%d/%Y') AS DATE) AS date,
    CAST(NULLIF(index_value, '') AS DOUBLE)                AS index_value
FROM "fhfa-mirs-transition-index"
WHERE NULLIF(release_date, '') IS NOT NULL
