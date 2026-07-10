-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Measure Code" AS measure_code,
    "Measure Description" AS measure_description,
    "Data Collection Period From Date" AS data_collection_period_from_date,
    strptime("Data Collection Period Through Date", '%m/%d/%Y')::DATE AS data_collection_period_through_date,
    "Measure Date Range" AS measure_date_range,
    strptime("Processing Date", '%Y%m%d')::DATE AS processing_date
FROM "cms-qmdc-9999"
