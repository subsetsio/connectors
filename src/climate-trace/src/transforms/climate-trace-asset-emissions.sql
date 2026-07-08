SELECT
    source_id,
    source_name,
    source_type,
    iso3_country,
    sector,
    subsector,
    gas,
    year,
    lat,
    lon,
    emissions_quantity,
    activity,
    activity_units,
    capacity,
    capacity_units
FROM "climate-trace-asset-emissions"
WHERE source_id IS NOT NULL
  AND year IS NOT NULL
