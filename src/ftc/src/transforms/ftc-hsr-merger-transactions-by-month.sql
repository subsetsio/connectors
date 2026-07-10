-- caution: Fiscal year-month rows use FTC fiscal-year numbering; month values are source-reported fiscal-period months, not derived calendar dates.
SELECT
    CAST("FYTransaction" AS BIGINT) AS fiscal_year,
    CAST("MonthTransaction" AS BIGINT) AS fiscal_month,
    CAST("TransactionReceived" AS BIGINT) AS transactions_received
FROM "ftc-hsr-merger-transactions-by-month"
