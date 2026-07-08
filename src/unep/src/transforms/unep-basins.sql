    SELECT
        CAST(year AS INTEGER)    AS year,
        CAST(pfaf_id AS BIGINT)  AS pfaf_id,
        CAST(level AS INTEGER)   AS basin_level,

CAST(permanent_sq_km           AS DOUBLE) AS permanent_sq_km,
CAST(projected_permanent_sq_km AS DOUBLE) AS projected_permanent_sq_km,
CAST(permanent_5yr_sq_km       AS DOUBLE) AS permanent_5yr_sq_km,
CAST(seasonal_sq_km            AS DOUBLE) AS seasonal_sq_km,
CAST(projected_seasonal_sq_km  AS DOUBLE) AS projected_seasonal_sq_km,
CAST(seasonal_5yr_sq_km        AS DOUBLE) AS seasonal_5yr_sq_km
    FROM "unep-basins"
    WHERE year IS NOT NULL
