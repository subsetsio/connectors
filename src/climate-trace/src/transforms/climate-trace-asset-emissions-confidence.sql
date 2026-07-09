SELECT
    source_id,
    source_name,
    iso3_country,
    sector,
    subsector,
    gas,
    year,
    source_type_confidence,
    capacity_confidence,
    capacity_factor_confidence,
    activity_confidence,
    emissions_factor_confidence,
    emissions_quantity_confidence
FROM "climate-trace-asset-emissions-confidence"
WHERE source_id IS NOT NULL
  AND year IS NOT NULL
