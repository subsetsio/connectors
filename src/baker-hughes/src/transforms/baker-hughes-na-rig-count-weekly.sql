SELECT DISTINCT
    CAST(publish_date AS DATE)   AS date,
    country, county, basin, gom, drill_for, location,
    state_province, trajectory,
    CAST(rig_count AS INTEGER)   AS rig_count
FROM "baker-hughes-na-rig-count-weekly"
WHERE publish_date IS NOT NULL AND rig_count IS NOT NULL
