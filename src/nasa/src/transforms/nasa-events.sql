-- EONET v3 natural-event tracker, flattened at download to one row per event
-- geometry. Types already carried by the NDJSON; publish with clean names.
SELECT
    "event_id" AS event_id,
    trim("title") AS title,
    "category_id" AS category_id,
    "category_title" AS category_title,
    "source_id" AS source_id,
    "date" AS observed_at,
    "geom_type" AS geom_type,
    "longitude" AS longitude,
    "latitude" AS latitude,
    "magnitude_value" AS magnitude_value,
    "magnitude_unit" AS magnitude_unit,
    "closed" AS closed_at
FROM "nasa-events"
