-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Period is a YYYYMM reference-period code stored by the source, not a date column.
-- caution: Rows are broken down by sovereign counterparty country, accounting portfolio, and maturity bucket; aggregate only across compatible dimensions.
SELECT
    "LEI_Code" AS lei_code,
    "NSA" AS nsa,
    CAST("Period" AS BIGINT) AS period,
    CAST("Item" AS BIGINT) AS item,
    "Label" AS label,
    CAST("Country" AS BIGINT) AS country,
    CAST("Accounting_portfolio" AS BIGINT) AS accounting_portfolio,
    CAST("Maturity" AS BIGINT) AS maturity,
    CAST("Amount" AS DOUBLE) AS amount,
    "Footnote" AS footnote,
    CAST("Row" AS BIGINT) AS row,
    CAST("Column" AS BIGINT) AS column,
    "Sheet" AS sheet
FROM "eba-te-sovereign-exposures"
