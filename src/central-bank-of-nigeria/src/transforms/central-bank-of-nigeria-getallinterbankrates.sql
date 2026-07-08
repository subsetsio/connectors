SELECT
            try_strptime(CAST("ratedate" AS VARCHAR), '%B-%d-%Y')::DATE AS "date",
            NULLIF(CAST("ratetype" AS VARCHAR), '') AS "ratetype",
            NULLIF(CAST("range" AS VARCHAR), '') AS "range",
            TRY_CAST(NULLIF(CAST("weightedaverage" AS VARCHAR), '') AS DOUBLE) AS "weightedaverage"
        FROM "central-bank-of-nigeria-getallinterbankrates"
