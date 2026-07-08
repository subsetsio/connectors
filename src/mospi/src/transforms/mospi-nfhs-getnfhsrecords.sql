SELECT
      * EXCLUDE ("value"),
      TRY_CAST("value" AS DOUBLE) AS "value"
    FROM "mospi-nfhs-getnfhsrecords"
