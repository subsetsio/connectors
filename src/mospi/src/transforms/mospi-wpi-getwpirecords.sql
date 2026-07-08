SELECT
      * EXCLUDE ("index_value"),
      TRY_CAST("index_value" AS DOUBLE) AS "index_value"
    FROM "mospi-wpi-getwpirecords"
