-- Statistics Canada table 34-10-0157 (CMHC).
-- Faithful pass-through of the raw asset: renames, casts, and a filter that drops
-- rows with no observation (StatCan suppresses them via STATUS, leaving VALUE null).
-- caution: the `geo` column mixes aggregation levels: national, provincial and roll-up rows (e.g. Canada, the provinces, 'Census metropolitan areas', 'All census agglomerations 50,000 and over') appear as ordinary rows alongside individual centres — filter `geo` before summing.
-- caution: `type_of_unit` mixes subtotals with their components — 'Multiples', 'Total units' overlap the component categories ('Apartment and other unit types', 'Row units', 'Semi-detached units', 'Single-detached units'); summing across the column double-counts. Pick one level.
-- caution: `value` is a 6-month moving average of monthly housing starts, not the starts observed in the reference month — consecutive rows overlap, so the column must not be summed to a period total.
-- caution: `value` is expressed in thousands of units (the source's SCALAR_FACTOR), not in single units — multiply by 1 000 for absolute figures.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    CAST("GEO" AS VARCHAR) AS geo,
    CAST("DGUID" AS VARCHAR) AS dguid,
    CAST("Type of unit" AS VARCHAR) AS type_of_unit,
    CAST("VALUE" AS DOUBLE) AS value,
    CAST("VECTOR" AS VARCHAR) AS vector,
    CAST("COORDINATE" AS VARCHAR) AS coordinate
FROM "cmhc-34100157"
WHERE "VALUE" IS NOT NULL
