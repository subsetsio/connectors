-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Period is a YYYYMM reference-period code stored by the source, not a date column.
-- caution: Rows are broken down by multiple credit-risk dimensions; aggregate only after selecting compatible portfolio, geography, exposure, performance-status, and NACE-code levels.
SELECT
    "LEI_Code" AS lei_code,
    "NSA" AS nsa,
    CAST("Period" AS BIGINT) AS period,
    CAST("Item" AS BIGINT) AS item,
    "Label" AS label,
    CAST("Portfolio" AS BIGINT) AS portfolio,
    CAST("Country" AS BIGINT) AS country,
    CAST("Country_rank" AS BIGINT) AS country_rank,
    CAST("Exposure" AS BIGINT) AS exposure,
    CAST("Status" AS BIGINT) AS status,
    CAST("Perf_Status" AS BIGINT) AS perf_status,
    CAST("NACE_codes" AS BIGINT) AS nace_codes,
    CAST("Amount" AS DOUBLE) AS amount,
    "Footnote" AS footnote,
    CAST("Row" AS BIGINT) AS row,
    CAST("Column" AS BIGINT) AS column,
    "Sheet" AS sheet
FROM "eba-te-credit-risk"
