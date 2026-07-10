-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Current employment is reported across multiple area, industry, series, and seasonal-adjustment dimensions; filter those dimensions before aggregating.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    CAST("Year" AS BIGINT) AS year,
    "Month" AS month,
    "Date" AS date,
    "Series Code" AS series_code,
    "Industry Title" AS industry_title,
    "Seasonally Adjusted (Y/N)" AS seasonally_adjusted_y_n,
    CAST("Current Employment" AS BIGINT) AS current_employment,
    CAST("Benchmark" AS BIGINT) AS benchmark
FROM "california-edd-2a5f872d-f7fe-49f2-9581-8f1b17ce5b90"
