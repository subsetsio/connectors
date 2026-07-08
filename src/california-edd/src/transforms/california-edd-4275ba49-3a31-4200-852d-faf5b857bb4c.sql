SELECT
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    TRY_CAST("Date" AS TIMESTAMP)::DATE AS date,
    TRY_CAST("Year" AS INTEGER) AS year,
    "Month" AS month,
    TRY_CAST(NULLIF(regexp_replace(CAST("Seasonally Adjusted" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS seasonally_adjusted,
    TRY_CAST(NULLIF(regexp_replace(CAST("Not Seasonally Adjusted" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS not_seasonally_adjusted
FROM "california-edd-4275ba49-3a31-4200-852d-faf5b857bb4c"
