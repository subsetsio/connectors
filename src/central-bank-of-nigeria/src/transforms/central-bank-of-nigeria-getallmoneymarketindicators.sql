SELECT
            CASE WHEN TRY_CAST(tmonth AS INTEGER) BETWEEN 1 AND 12 THEN make_date(TRY_CAST(tyear AS INTEGER), TRY_CAST(tmonth AS INTEGER), 1) WHEN TRY_CAST(tyear AS INTEGER) BETWEEN 1900 AND 2100 THEN make_date(TRY_CAST(tyear AS INTEGER), 12, 31) ELSE NULL END AS "date",
            NULLIF(CAST("period" AS VARCHAR), '') AS "period",
            TRY_CAST(NULLIF(CAST("interBankCallRate" AS VARCHAR), '') AS DOUBLE) AS "interBankCallRate",
            TRY_CAST(NULLIF(CAST("mrr" AS VARCHAR), '') AS DOUBLE) AS "mrr",
            TRY_CAST(NULLIF(CAST("mpr" AS VARCHAR), '') AS DOUBLE) AS "mpr",
            TRY_CAST(NULLIF(CAST("treasuryBill" AS VARCHAR), '') AS DOUBLE) AS "treasuryBill",
            TRY_CAST(NULLIF(CAST("savingsDeposit" AS VARCHAR), '') AS DOUBLE) AS "savingsDeposit",
            TRY_CAST(NULLIF(CAST("oneMonthDeposit" AS VARCHAR), '') AS DOUBLE) AS "oneMonthDeposit",
            TRY_CAST(NULLIF(CAST("threeMonthsDeposit" AS VARCHAR), '') AS DOUBLE) AS "threeMonthsDeposit",
            TRY_CAST(NULLIF(CAST("sixMonthsDeposit" AS VARCHAR), '') AS DOUBLE) AS "sixMonthsDeposit",
            TRY_CAST(NULLIF(CAST("twelveMonthsDeposit" AS VARCHAR), '') AS DOUBLE) AS "twelveMonthsDeposit",
            TRY_CAST(NULLIF(CAST("primeLending" AS VARCHAR), '') AS DOUBLE) AS "primeLending",
            TRY_CAST(NULLIF(CAST("maxLending" AS VARCHAR), '') AS DOUBLE) AS "maxLending"
        FROM "central-bank-of-nigeria-getallmoneymarketindicators"
