SELECT * FROM (
    SELECT
        TRY_CAST(FYTransaction AS INTEGER)       AS fiscal_year,
        TRY_CAST(MonthTransaction AS INTEGER)    AS month,
        TRY_CAST(TransactionReceived AS INTEGER) AS transactions_received
    FROM "ftc-hsr-merger-transactions-by-month"
)
WHERE fiscal_year IS NOT NULL AND transactions_received IS NOT NULL
