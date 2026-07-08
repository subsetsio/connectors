SELECT
    "Area Name" AS area_name,
    "Area Type" AS area_type,
    TRY_CAST("Year" AS INTEGER) AS year,
    "Month" AS month,
    "Seasonally Adjusted(Y/N)" AS seasonally_adjusted,
    "Status" AS status,
    TRY_CAST(NULLIF(regexp_replace(CAST("Labor Force" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS labor_force,
    TRY_CAST(NULLIF(regexp_replace(CAST("Employment" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS employment,
    TRY_CAST(NULLIF(regexp_replace(CAST("Unemployment" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS unemployment,
    TRY_CAST(NULLIF(regexp_replace(CAST("Unemployment Rate" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS unemployment_rate
FROM "california-edd-74b655ae-6158-41ab-81ef-a02984a17cc1"
