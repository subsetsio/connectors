-- Statistics Canada table 34-10-0150 (CMHC).
-- Faithful pass-through of the raw asset: renames, casts, and a filter that drops
-- rows with no observation (StatCan suppresses them via STATUS, leaving VALUE null).
-- caution: the `geo` column mixes aggregation levels: national, provincial and roll-up rows (e.g. Canada, the provinces, 'Census metropolitan areas', 'All census agglomerations 50,000 and over') appear as ordinary rows alongside individual centres — filter `geo` before summing.
-- caution: `completed_dwelling_units` stacks a flow (absorptions during the period) and a stock (unabsorbed inventory at period end) in one value column — never sum across this column.
-- caution: `type_of_dwelling_unit` mixes subtotals with their components — 'Total units' overlap the component categories ('Semi-detached units', 'Single detached units'); summing across the column double-counts. Pick one level.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    CAST("GEO" AS VARCHAR) AS geo,
    CAST("DGUID" AS VARCHAR) AS dguid,
    CAST("Completed dwelling units" AS VARCHAR) AS completed_dwelling_units,
    CAST("Type of dwelling unit" AS VARCHAR) AS type_of_dwelling_unit,
    CAST("VALUE" AS DOUBLE) AS value,
    COALESCE(CAST("TERMINATED" AS VARCHAR) = 't', FALSE) AS terminated,
    CAST("VECTOR" AS VARCHAR) AS vector,
    CAST("COORDINATE" AS VARCHAR) AS coordinate
FROM "cmhc-34100150"
WHERE "VALUE" IS NOT NULL
