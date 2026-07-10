-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Period is a YYYYMM reference-period code stored by the source, not a date column.
-- caution: Market-risk rows are split by portfolio, model/product, and risk category; aggregate only across compatible levels.
SELECT
    "LEI_Code" AS lei_code,
    "NSA" AS nsa,
    CAST("Period" AS BIGINT) AS period,
    CAST("Item" AS BIGINT) AS item,
    "Label" AS label,
    CAST("Portfolio" AS BIGINT) AS portfolio,
    CAST("MKT_Modprod" AS BIGINT) AS mkt_modprod,
    CAST("Mkt_risk" AS BIGINT) AS mkt_risk,
    CAST("Amount" AS DOUBLE) AS amount,
    "Footnote" AS footnote,
    CAST("Row" AS BIGINT) AS row,
    CAST("Column" AS BIGINT) AS column,
    "Sheet" AS sheet
FROM "eba-te-market-risk"
