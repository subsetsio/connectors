SELECT
    station_id,
    CAST(observed_at AS TIMESTAMPTZ) AS observed_at,
    element, value, quality_flag
FROM "japan-meteorological-agency-amedas-observations"
WHERE station_id IS NOT NULL AND element IS NOT NULL AND value IS NOT NULL
