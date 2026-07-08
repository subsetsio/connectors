SELECT
    iso_code3,
    country,
    global_category,
    overview_category,
    sector,
    subsector,
    indicator_id,
    indicator_name,
    source,
    value
FROM "wri-ndc-content"
WHERE indicator_id IS NOT NULL
