-- caution: Annual HSR measures mix transaction counts, filing counts, second requests, and early termination outcomes; the upstream CSV includes blank separator rows that are not observations, and percentage columns should not be summed.
SELECT
    CAST(REPLACE("FY", ',', '') AS BIGINT) AS fiscal_year,
    CAST(REPLACE("TransactionsReported", ',', '') AS BIGINT) AS transactions_reported,
    CAST(REPLACE("FilingsReceived", ',', '') AS BIGINT) AS filings_received,
    CAST(REPLACE("AdjustedTransactions", ',', '') AS BIGINT) AS adjusted_transactions,
    CAST(REPLACE("SecondRequestTotal", ',', '') AS BIGINT) AS second_request_total,
    CAST(REPLACE("SecondRequestFTC", ',', '') AS BIGINT) AS second_request_ftc,
    CAST("SecondRequestPercentFTC" AS DOUBLE) AS second_request_percent_ftc,
    CAST(REPLACE("SecondRequestDOJ", ',', '') AS BIGINT) AS second_request_doj,
    CAST("SecondRequestPercentDOJ" AS DOUBLE) AS second_request_percent_doj,
    CAST(REPLACE("EarlyTerminationTransactions", ',', '') AS BIGINT) AS early_termination_transactions,
    CAST(REPLACE("EarlyTerminationTransactionsGranted", ',', '') AS BIGINT) AS early_termination_transactions_granted,
    CAST(REPLACE("EarlyTerminationTransactionsNotGranted", ',', '') AS BIGINT) AS early_termination_transactions_not_granted
FROM "ftc-hsr-transactions-filings-second-requests-by-fy"
WHERE NULLIF(TRIM("FY"), '') IS NOT NULL
