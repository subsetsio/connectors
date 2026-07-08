SELECT DISTINCT
    CAST(date AS DATE)           AS date,
    region,
    CAST(rig_count AS INTEGER)   AS rig_count
FROM "baker-hughes-worldwide-rig-count-historical-monthly"
WHERE date IS NOT NULL AND rig_count IS NOT NULL
