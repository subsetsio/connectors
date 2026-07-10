-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Fiscal year-month rows use FTC fiscal-year numbering; month values are source-reported fiscal-period months, not derived calendar dates.
SELECT
    CAST("FYTransaction" AS BIGINT) AS fytransaction,
    CAST("MonthTransaction" AS BIGINT) AS monthtransaction,
    CAST("TransactionReceived" AS BIGINT) AS transactionreceived
FROM "ftc-hsr-merger-transactions-by-month"
