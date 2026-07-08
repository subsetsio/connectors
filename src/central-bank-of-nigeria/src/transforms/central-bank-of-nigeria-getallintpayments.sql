SELECT
            try_strptime(CAST("payDate" AS VARCHAR), '%d/%m/%Y')::DATE AS "date",
            TRY_CAST(NULLIF(CAST("loc" AS VARCHAR), '') AS DOUBLE) AS "loc",
            TRY_CAST(NULLIF(CAST("remit" AS VARCHAR), '') AS DOUBLE) AS "remit",
            TRY_CAST(NULLIF(CAST("debt" AS VARCHAR), '') AS DOUBLE) AS "debt",
            TRY_CAST(NULLIF(CAST("total" AS VARCHAR), '') AS DOUBLE) AS "total"
        FROM "central-bank-of-nigeria-getallintpayments"
