SELECT
            try_strptime(CAST("postDate" AS VARCHAR), '%d/%m/%Y')::DATE AS "date",
            TRY_CAST(NULLIF(CAST("crudeOilPrice" AS VARCHAR), '') AS DOUBLE) AS "crudeOilPrice"
        FROM "central-bank-of-nigeria-getalldailycrude"
