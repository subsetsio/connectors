-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Period is a YYYYMM reference-period code stored by the source, not a date column.
-- caution: This table combines several non-credit/non-market/non-sovereign Transparency Exercise templates; filter the template or item family before aggregation.
SELECT
    "LEI_Code" AS lei_code,
    "NSA" AS nsa,
    CAST("Period" AS BIGINT) AS period,
    CAST("Item" AS BIGINT) AS item,
    "Label" AS label,
    CAST("ASSETS_FV" AS BIGINT) AS assets_fv,
    CAST("ASSETS_Stages" AS BIGINT) AS assets_stages,
    CAST("Exposure" AS BIGINT) AS exposure,
    CAST("Financial_instruments" AS BIGINT) AS financial_instruments,
    CAST("Amount" AS DOUBLE) AS amount,
    CAST("Fin_end_year" AS BIGINT) AS fin_end_year,
    CAST("n_quarters" AS BIGINT) AS n_quarters,
    "Footnote" AS footnote,
    CAST("Row" AS BIGINT) AS row,
    CAST("Column" AS BIGINT) AS column,
    "Sheet" AS sheet
FROM "eba-te-other-exposures"
