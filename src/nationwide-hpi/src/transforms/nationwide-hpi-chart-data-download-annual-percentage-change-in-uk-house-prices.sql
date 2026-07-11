-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a frozen chart-data export; the continuing UK annual percentage change appears in the live monthly and quarterly series.
SELECT
    "date",
    strptime("period_label", '%Y-%m-%d')::DATE AS period_label,
    "category",
    "measure",
    "value"
FROM "nationwide-hpi-chart-data-download-annual-percentage-change-in-uk-house-prices"
