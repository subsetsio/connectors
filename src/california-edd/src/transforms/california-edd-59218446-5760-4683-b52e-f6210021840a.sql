SELECT
    "Area Name" AS area_name,
    "Area Type" AS area_type,
    TRY_CAST("Year" AS INTEGER) AS year,
    "Month" AS month,
    "Date_Numeric" AS date_numeric,
    "Seasonally Adjusted(Y/N)" AS seasonally_adjusted,
    "Status" AS status,
    TRY_CAST(NULLIF(regexp_replace(CAST("Labor Force" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS labor_force,
    TRY_CAST(NULLIF(regexp_replace(CAST("Employment" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS employment,
    TRY_CAST(NULLIF(regexp_replace(CAST("Unemployment" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS unemployment,
    TRY_CAST(NULLIF(regexp_replace(CAST("Unemployment Rate" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS unemployment_rate,
    "Benchmark" AS benchmark
FROM "california-edd-59218446-5760-4683-b52e-f6210021840a"
