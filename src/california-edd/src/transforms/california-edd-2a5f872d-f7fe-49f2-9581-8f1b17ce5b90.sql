SELECT
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    TRY_CAST("Year" AS INTEGER) AS year,
    "Month" AS month,
    try_strptime("Date", '%m/%d/%Y')::DATE AS date,
    "Series Code" AS series_code,
    "Industry Title" AS industry_title,
    "Seasonally Adjusted (Y/N)" AS seasonally_adjusted,
    TRY_CAST(NULLIF(regexp_replace(CAST("Current Employment" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS current_employment,
    TRY_CAST("Benchmark" AS INTEGER) AS benchmark
FROM "california-edd-2a5f872d-f7fe-49f2-9581-8f1b17ce5b90"
