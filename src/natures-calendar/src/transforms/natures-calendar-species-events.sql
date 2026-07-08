SELECT
    CAST(species_id AS BIGINT)  AS species_id,
    CAST(event_id   AS BIGINT)  AS event_id,
    species_name,
    latin_name,
    nbn_taxonomy,
    species_group,
    event_name,
    event_type,
    CAST(range_month_from AS INTEGER) AS expected_month_from,
    CAST(range_day_from   AS INTEGER) AS expected_day_from,
    CAST(range_month_to   AS INTEGER) AS expected_month_to,
    CAST(range_day_to     AS INTEGER) AS expected_day_to
FROM "natures-calendar-species-events"
WHERE species_id IS NOT NULL AND event_id IS NOT NULL
