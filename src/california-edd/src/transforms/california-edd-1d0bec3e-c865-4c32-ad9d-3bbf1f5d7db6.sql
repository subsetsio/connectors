SELECT
    "Date" AS date,
    TRY_CAST("Year" AS INTEGER) AS year,
    "Month" AS month,
    TRY_CAST(NULLIF(regexp_replace(CAST("California Labor Force Participation Rate" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS ca_lfpr,
    TRY_CAST(NULLIF(regexp_replace(CAST("US Labor Force Participation Rate" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS us_lfpr
FROM "california-edd-1d0bec3e-c865-4c32-ad9d-3bbf1f5d7db6"
