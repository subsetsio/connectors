SELECT DISTINCT
    make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
    region, country, drill_for, location, rig_status,
    CAST(rig_count AS INTEGER)   AS rig_count
FROM "baker-hughes-worldwide-rig-count-monthly"
WHERE year IS NOT NULL AND month IS NOT NULL AND rig_count IS NOT NULL
