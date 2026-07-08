SELECT
      * EXCLUDE ("current_price", "constant_price"),
      TRY_CAST("current_price" AS DOUBLE) AS "current_price",
      TRY_CAST("constant_price" AS DOUBLE) AS "constant_price"
    FROM "mospi-nas-getnasdata"
