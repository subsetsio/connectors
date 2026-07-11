-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is the UK monthly series; use the quarterly or regional tables for regional comparisons.
SELECT
    "date",
    strptime("period_label", '%Y-%m-%d')::DATE AS period_label,
    "category",
    "measure",
    "value"
FROM "nationwide-hpi-monthly"
