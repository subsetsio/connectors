SELECT
    state,
    station_slug,
    station_name,
    CAST(date AS DATE)              AS date,
    evapotranspiration_mm,
    rainfall_mm,
    pan_evaporation_mm,
    max_temp_c,
    min_temp_c,
    max_relative_humidity_pct,
    min_relative_humidity_pct,
    wind_speed_ms,
    solar_radiation_mj_m2
FROM "bom-daily-weather-observations"
WHERE date IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY station_slug, date ORDER BY station_name
) = 1
