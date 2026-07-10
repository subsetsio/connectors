-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Period is a YYYYMM scenario/reference code stored by the source, not a date column.
-- caution: Scenario is source-coded; use the source scenario definitions before comparing baseline, adverse, actual, and restated rows.
SELECT
    "Country_code" AS country_code,
    "LEI_Code" AS lei_code,
    "Bank_name" AS bank_name,
    CAST("Period" AS BIGINT) AS period,
    CAST("Item" AS BIGINT) AS item,
    CAST("Scenario" AS BIGINT) AS scenario,
    "Fact_char" AS fact_char,
    CAST("Amount" AS DOUBLE) AS amount
FROM "eba-stress-test-results"
