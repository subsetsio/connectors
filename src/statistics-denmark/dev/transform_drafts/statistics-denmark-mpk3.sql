SELECT
    * EXCLUDE (INDHOLD),
    TRY_CAST(NULLIF(NULLIF(TRIM(INDHOLD), '..'), '.') AS DOUBLE) AS value
FROM "statistics-denmark-mpk3"
