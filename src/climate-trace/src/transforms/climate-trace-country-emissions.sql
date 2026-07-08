SELECT
    iso3_country,
    sector,
    subsector,
    gas,
    CAST(start_time AS TIMESTAMP)        AS period_start,
    CAST(end_time   AS TIMESTAMP)        AS period_end,
    CAST(substr(start_time, 1, 4) AS INTEGER) AS year,
    temporal_granularity,
    CAST(emissions_quantity AS DOUBLE)   AS emissions_quantity,
    emissions_quantity_units             AS units
FROM "climate-trace-country-emissions"
WHERE emissions_quantity IS NOT NULL
  AND iso3_country IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY iso3_country, subsector, gas, start_time, temporal_granularity
    ORDER BY modified_date DESC
) = 1
