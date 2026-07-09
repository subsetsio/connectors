-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are long-form PBOC line items; this source table has repeated line-item context in the raw columns, so do not assume one row per period and `item`.
SELECT
    "item",
    strptime("period", '%Y-%m')::DATE AS period,
    "year",
    "month",
    "value",
    "unit",
    "source_year"
FROM "people-s-bank-of-china-aggregate-financing-to-the-real-economy--aggregate-financing-to-the-real-economy-flow"
