-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Annual HSR measures mix transaction counts, filing counts, second requests, and early termination outcomes; the upstream CSV includes blank separator rows that are not observations, and percentage columns should not be summed.
SELECT
    "FY" AS fy,
    "TransactionsReported" AS transactionsreported,
    "FilingsReceived" AS filingsreceived,
    "AdjustedTransactions" AS adjustedtransactions,
    "SecondRequestTotal" AS secondrequesttotal,
    "SecondRequestFTC" AS secondrequestftc,
    "SecondRequestPercentFTC" AS secondrequestpercentftc,
    "SecondRequestDOJ" AS secondrequestdoj,
    "SecondRequestPercentDOJ" AS secondrequestpercentdoj,
    "EarlyTerminationTransactions" AS earlyterminationtransactions,
    "EarlyTerminationTransactionsGranted" AS earlyterminationtransactionsgranted,
    "EarlyTerminationTransactionsNotGranted" AS earlyterminationtransactionsnotgranted
FROM "ftc-hsr-transactions-filings-second-requests-by-fy"
