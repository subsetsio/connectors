    SELECT
        CAST(year AS INTEGER)      AS year,
        CAST(adm0_code AS BIGINT)  AS adm0_code,
        country_name,
        CAST(adm1_code AS BIGINT)  AS adm1_code,
        region_name,

CAST(permanent_sq_km           AS DOUBLE) AS permanent_sq_km,
CAST(projected_permanent_sq_km AS DOUBLE) AS projected_permanent_sq_km,
CAST(permanent_5yr_sq_km       AS DOUBLE) AS permanent_5yr_sq_km,
CAST(seasonal_sq_km            AS DOUBLE) AS seasonal_sq_km,
CAST(projected_seasonal_sq_km  AS DOUBLE) AS projected_seasonal_sq_km,
CAST(seasonal_5yr_sq_km        AS DOUBLE) AS seasonal_5yr_sq_km
    FROM "unep-subnational-adm1"
    WHERE year IS NOT NULL
