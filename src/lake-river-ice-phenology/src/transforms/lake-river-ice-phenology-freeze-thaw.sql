SELECT
    lakecode,
    lakename,
    lakeorriver,
    season,
    TRY_CAST(NULLIF(iceon_year,  '-999') AS INTEGER) AS iceon_year,
    TRY_CAST(NULLIF(iceon_month, '-999') AS INTEGER) AS iceon_month,
    TRY_CAST(NULLIF(iceon_day,   '-999') AS INTEGER) AS iceon_day,
    TRY_CAST(NULLIF(iceoff_year,  '-999') AS INTEGER) AS iceoff_year,
    TRY_CAST(NULLIF(iceoff_month, '-999') AS INTEGER) AS iceoff_month,
    TRY_CAST(NULLIF(iceoff_day,   '-999') AS INTEGER) AS iceoff_day,
    TRY_CAST(NULLIF(duration, '-999') AS INTEGER) AS duration_days,
    TRY_CAST(latitude  AS DOUBLE) AS latitude,
    TRY_CAST(longitude AS DOUBLE) AS longitude,
    country,
    froze,
    NULLIF(comments, '') AS comments
FROM "lake-river-ice-phenology-freeze-thaw"
WHERE lakecode IS NOT NULL AND season IS NOT NULL
