SELECT * FROM (
    SELECT
        TRY_CAST(FY AS INTEGER)                              AS fiscal_year,
        TRY_CAST(TransactionsReported AS INTEGER)            AS transactions_reported,
        TRY_CAST(FilingsReceived AS INTEGER)                 AS filings_received,
        TRY_CAST(AdjustedTransactions AS INTEGER)            AS adjusted_transactions,
        TRY_CAST(SecondRequestTotal AS INTEGER)              AS second_request_total,
        TRY_CAST(SecondRequestFTC AS INTEGER)                AS second_request_ftc,
        TRY_CAST(SecondRequestPercentFTC AS DOUBLE)          AS second_request_percent_ftc,
        TRY_CAST(SecondRequestDOJ AS INTEGER)                AS second_request_doj,
        TRY_CAST(SecondRequestPercentDOJ AS DOUBLE)          AS second_request_percent_doj,
        TRY_CAST(EarlyTerminationTransactions AS INTEGER)    AS early_termination_transactions,
        TRY_CAST(EarlyTerminationTransactionsGranted AS INTEGER)    AS early_termination_granted,
        TRY_CAST(EarlyTerminationTransactionsNotGranted AS INTEGER) AS early_termination_not_granted
    FROM "ftc-hsr-transactions-filings-second-requests-by-fy"
)
WHERE fiscal_year IS NOT NULL
