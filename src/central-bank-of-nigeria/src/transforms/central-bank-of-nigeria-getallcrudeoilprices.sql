SELECT
            CASE WHEN TRY_CAST(tmonth AS INTEGER) BETWEEN 1 AND 12 THEN make_date(TRY_CAST(tyear AS INTEGER), TRY_CAST(tmonth AS INTEGER), 1) WHEN TRY_CAST(tyear AS INTEGER) BETWEEN 1900 AND 2100 THEN make_date(TRY_CAST(tyear AS INTEGER), 12, 31) ELSE NULL END AS "date",
            NULLIF(CAST("period" AS VARCHAR), '') AS "period",
            TRY_CAST(NULLIF(CAST("crudeOilPrice" AS VARCHAR), '') AS DOUBLE) AS "crudeOilPrice",
            TRY_CAST(NULLIF(CAST("domProd" AS VARCHAR), '') AS DOUBLE) AS "domProd",
            TRY_CAST(NULLIF(CAST("crudeOilExp" AS VARCHAR), '') AS DOUBLE) AS "crudeOilExp"
        FROM "central-bank-of-nigeria-getallcrudeoilprices"
