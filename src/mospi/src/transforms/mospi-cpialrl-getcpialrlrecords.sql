SELECT
      * EXCLUDE ("index_al", "index_rl", "inflation_al", "inflation_rl"),
      TRY_CAST("index_al" AS DOUBLE) AS "index_al",
      TRY_CAST("index_rl" AS DOUBLE) AS "index_rl",
      TRY_CAST("inflation_al" AS DOUBLE) AS "inflation_al",
      TRY_CAST("inflation_rl" AS DOUBLE) AS "inflation_rl"
    FROM "mospi-cpialrl-getcpialrlrecords"
