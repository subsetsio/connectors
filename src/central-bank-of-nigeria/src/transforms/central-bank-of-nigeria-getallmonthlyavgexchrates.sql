SELECT
            CASE WHEN TRY_CAST(tmonth AS INTEGER) BETWEEN 1 AND 12 THEN make_date(TRY_CAST(tyear AS INTEGER), TRY_CAST(tmonth AS INTEGER), 1) WHEN TRY_CAST(tyear AS INTEGER) BETWEEN 1900 AND 2100 THEN make_date(TRY_CAST(tyear AS INTEGER), 12, 31) ELSE NULL END AS "date",
            NULLIF(CAST("period" AS VARCHAR), '') AS "period",
            TRY_CAST(NULLIF(CAST("daswdasDollar" AS VARCHAR), '') AS DOUBLE) AS "daswdasDollar",
            TRY_CAST(NULLIF(CAST("ifemDollar" AS VARCHAR), '') AS DOUBLE) AS "ifemDollar",
            TRY_CAST(NULLIF(CAST("bdcDollar" AS VARCHAR), '') AS DOUBLE) AS "bdcDollar",
            TRY_CAST(NULLIF(CAST("pounds" AS VARCHAR), '') AS DOUBLE) AS "pounds",
            TRY_CAST(NULLIF(CAST("euro" AS VARCHAR), '') AS DOUBLE) AS "euro",
            TRY_CAST(NULLIF(CAST("cfaFr" AS VARCHAR), '') AS DOUBLE) AS "cfaFr"
        FROM "central-bank-of-nigeria-getallmonthlyavgexchrates"
