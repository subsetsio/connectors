SELECT
            CASE WHEN TRY_CAST(tmonth AS INTEGER) BETWEEN 1 AND 12 THEN make_date(TRY_CAST(tyear AS INTEGER), TRY_CAST(tmonth AS INTEGER), 1) WHEN TRY_CAST(tyear AS INTEGER) BETWEEN 1900 AND 2100 THEN make_date(TRY_CAST(tyear AS INTEGER), 12, 31) ELSE NULL END AS "date",
            NULLIF(CAST("period" AS VARCHAR), '') AS "period",
            TRY_CAST(NULLIF(CAST("allItemsYearOn" AS VARCHAR), '') AS DOUBLE) AS "allItemsYearOn",
            TRY_CAST(NULLIF(CAST("allItemsAverage" AS VARCHAR), '') AS DOUBLE) AS "allItemsAverage",
            TRY_CAST(NULLIF(CAST("foodYearOn" AS VARCHAR), '') AS DOUBLE) AS "foodYearOn",
            TRY_CAST(NULLIF(CAST("foodAverage" AS VARCHAR), '') AS DOUBLE) AS "foodAverage",
            TRY_CAST(NULLIF(CAST("allItemsLessFrmProdYearOn" AS VARCHAR), '') AS DOUBLE) AS "allItemsLessFrmProdYearOn",
            TRY_CAST(NULLIF(CAST("allItemsLessFrmProdAverage" AS VARCHAR), '') AS DOUBLE) AS "allItemsLessFrmProdAverage",
            TRY_CAST(NULLIF(CAST("allItemsLessFrmProdAndEnergyYearOn" AS VARCHAR), '') AS DOUBLE) AS "allItemsLessFrmProdAndEnergyYearOn",
            TRY_CAST(NULLIF(CAST("allItemsLessFrmProdAndEnergyAvg" AS VARCHAR), '') AS DOUBLE) AS "allItemsLessFrmProdAndEnergyAvg"
        FROM "central-bank-of-nigeria-getallinflationrates"
