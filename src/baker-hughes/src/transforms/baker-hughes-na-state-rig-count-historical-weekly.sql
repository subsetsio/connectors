SELECT DISTINCT
    CAST(date AS DATE)           AS date,
    area, category, location_label,
    CAST(rig_count AS INTEGER)   AS rig_count
FROM "baker-hughes-na-state-rig-count-historical-weekly"
WHERE date IS NOT NULL AND rig_count IS NOT NULL
