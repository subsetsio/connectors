SELECT
            try_strptime(CAST("ratedate" AS VARCHAR), '%d/%m/%Y')::DATE AS "date",
            NULLIF(CAST("ratetype" AS VARCHAR), '') AS "ratetype",
            TRY_CAST(NULLIF(CAST("amount" AS VARCHAR), '') AS DOUBLE) AS "amount"
        FROM "central-bank-of-nigeria-getalldiscountrates"
