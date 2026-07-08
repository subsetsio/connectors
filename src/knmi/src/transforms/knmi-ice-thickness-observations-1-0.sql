SELECT location,
       CAST(year AS INTEGER) AS year,
       TRY_STRPTIME(date, '%m/%d/%Y')::DATE AS obs_date,
       CAST(latitude AS DOUBLE) AS latitude,
       CAST(longitude AS DOUBLE) AS longitude,
       NULLIF(CAST(water_depth_m AS DOUBLE), 999) AS water_depth_m,
       NULLIF(CAST(ice_depth_cm AS DOUBLE), 999) AS ice_depth_cm,
       NULLIF(CAST(snow_depth_cm AS DOUBLE), 999) AS snow_depth_cm,  -- 999 = KNMI missing-value code
       observer
FROM "knmi-ice-thickness-observations-1-0"
WHERE date IS NOT NULL
