SELECT * EXCLUDE ("Footnote", "Row", "Column", "Sheet")
    REPLACE (
        CAST("Period" AS INTEGER) AS "Period",
        TRY_CAST("Amount" AS DOUBLE) AS "Amount"
    )
FROM "eba-te-credit-risk"
WHERE TRY_CAST("Amount" AS DOUBLE) IS NOT NULL
