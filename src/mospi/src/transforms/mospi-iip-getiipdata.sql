SELECT
      * EXCLUDE ("index", "growth_rate"),
      TRY_CAST("index" AS DOUBLE) AS "index",
      TRY_CAST("growth_rate" AS DOUBLE) AS "growth_rate"
    FROM "mospi-iip-getiipdata"
