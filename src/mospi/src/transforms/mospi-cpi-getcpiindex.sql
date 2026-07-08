SELECT
      * EXCLUDE ("index", "inflation"),
      TRY_CAST("index" AS DOUBLE) AS "index",
      TRY_CAST("inflation" AS DOUBLE) AS "inflation"
    FROM "mospi-cpi-getcpiindex"
