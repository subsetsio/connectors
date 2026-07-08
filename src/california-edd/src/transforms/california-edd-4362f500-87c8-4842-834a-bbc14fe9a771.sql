SELECT
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Date" AS date,
    TRY_CAST("Year" AS INTEGER) AS year,
    "Month" AS month,
    TRY_CAST(NULLIF(regexp_replace(CAST("Age 16-19" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS age_16_19,
    TRY_CAST(NULLIF(regexp_replace(CAST("Age 20-24" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS age_20_24,
    TRY_CAST(NULLIF(regexp_replace(CAST("Age 25-34" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS age_25_34,
    TRY_CAST(NULLIF(regexp_replace(CAST("Age 35-44" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS age_35_44,
    TRY_CAST(NULLIF(regexp_replace(CAST("Age 45-54" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS age_45_54,
    TRY_CAST(NULLIF(regexp_replace(CAST("Age 55-64" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS age_55_64,
    TRY_CAST(NULLIF(regexp_replace(CAST("Age 65+" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS age_65_plus
FROM "california-edd-4362f500-87c8-4842-834a-bbc14fe9a771"
