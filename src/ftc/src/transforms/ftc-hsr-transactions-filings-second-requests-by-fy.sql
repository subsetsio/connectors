-- caution: Annual HSR measures mix transaction counts, filing counts, second requests, and early termination outcomes; the upstream CSV includes blank separator rows that are not observations, and percentage columns should not be summed.
SELECT
    CAST("FY" AS BIGINT) AS fiscal_year,
    CAST("TransactionsReported" AS BIGINT) AS transactions_reported,
    CAST("FilingsReceived" AS BIGINT) AS filings_received,
    CAST("AdjustedTransactions" AS BIGINT) AS adjusted_transactions,
    CAST("SecondRequestTotal" AS BIGINT) AS second_request_total,
    CAST("SecondRequestFTC" AS BIGINT) AS second_request_ftc,
    CAST("SecondRequestPercentFTC" AS DOUBLE) AS second_request_percent_ftc,
    CAST("SecondRequestDOJ" AS BIGINT) AS second_request_doj,
    CAST("SecondRequestPercentDOJ" AS DOUBLE) AS second_request_percent_doj,
    CAST("EarlyTerminationTransactions" AS BIGINT) AS early_termination_transactions,
    CAST("EarlyTerminationTransactionsGranted" AS BIGINT) AS early_termination_transactions_granted,
    CAST("EarlyTerminationTransactionsNotGranted" AS BIGINT) AS early_termination_transactions_not_granted
FROM "ftc-hsr-transactions-filings-second-requests-by-fy"
WHERE NULLIF(TRIM("FY"), '') IS NOT NULL
