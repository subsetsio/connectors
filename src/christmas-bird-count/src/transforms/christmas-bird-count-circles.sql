SELECT
    circle_id,
    circle_name,
    abbrev,
    latitude,
    longitude
FROM "christmas-bird-count-circles"
WHERE circle_id IS NOT NULL
