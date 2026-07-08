SELECT
            try_strptime(CAST("moveDate" AS VARCHAR), '%d/%m/%Y')::DATE AS "date",
            TRY_CAST(NULLIF(CAST("gross" AS VARCHAR), '') AS DOUBLE) AS "gross",
            TRY_CAST(NULLIF(CAST("liquid" AS VARCHAR), '') AS DOUBLE) AS "liquid",
            TRY_CAST(NULLIF(CAST("blocked" AS VARCHAR), '') AS DOUBLE) AS "blocked",
            TRY_CAST(NULLIF(CAST("blockPercent" AS VARCHAR), '') AS DOUBLE) AS "blockPercent"
        FROM "central-bank-of-nigeria-getallreserves"
