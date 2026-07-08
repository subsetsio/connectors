SELECT DISTINCT
    make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
    country, county, basin, gom, drill_for, location,
    state_province, trajectory,
    CAST(rig_count AS DOUBLE)    AS rig_count
FROM "baker-hughes-na-rig-count-monthly"
WHERE year IS NOT NULL AND month IS NOT NULL AND rig_count IS NOT NULL
