SELECT
    notation,
    label,
    description,
    county,
    ea_area_name,
    river_or_sea,
    fwd_code,
    quick_dial_number,
    TRY_CAST(lat AS DOUBLE)  AS lat,
    TRY_CAST(long AS DOUBLE) AS lon
FROM "defra-flood-monitoring-floods"
WHERE notation IS NOT NULL AND notation <> ''
