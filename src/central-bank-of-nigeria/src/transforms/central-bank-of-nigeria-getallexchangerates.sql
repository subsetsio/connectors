SELECT
            TRY_CAST(NULLIF(CAST("ratedate" AS VARCHAR), '') AS DATE) AS "date",
            NULLIF(CAST("currency" AS VARCHAR), '') AS "currency",
            TRY_CAST(NULLIF(CAST("buyingrate" AS VARCHAR), '') AS DOUBLE) AS "buyingrate",
            TRY_CAST(NULLIF(CAST("centralrate" AS VARCHAR), '') AS DOUBLE) AS "centralrate",
            TRY_CAST(NULLIF(CAST("sellingrate" AS VARCHAR), '') AS DOUBLE) AS "sellingrate"
        FROM "central-bank-of-nigeria-getallexchangerates"
