-- Statistics Canada table 34-10-0096 (CMHC).
-- Faithful pass-through of the raw asset: renames, casts, and a filter that drops
-- rows with no observation (StatCan suppresses them via STATUS, leaving VALUE null).
-- caution: the `geo` column mixes aggregation levels: national, provincial and roll-up rows (e.g. Canada, the provinces, 'Census metropolitan areas', 'All census agglomerations 50,000 and over') appear as ordinary rows alongside individual centres — filter `geo` before summing.
-- caution: `type_of_unit` mixes subtotals with their components — 'Total semi, row, apartment and other unit types', 'Total units' overlap the component categories ('All other types of units', 'Single-detached units'); summing across the column double-counts. Pick one level.
-- caution: `value` is a seasonally adjusted model estimate, not a raw count of dwelling units — it is not comparable with the unadjusted counts published in the other tables of this source.
-- caution: `value` is expressed in thousands of units (the source's SCALAR_FACTOR), not in single units — multiply by 1 000 for absolute figures.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    CAST("GEO" AS VARCHAR) AS geo,
    CAST("DGUID" AS VARCHAR) AS dguid,
    CAST("Type of unit" AS VARCHAR) AS type_of_unit,
    CAST("VALUE" AS DOUBLE) AS value,
    COALESCE(CAST("TERMINATED" AS VARCHAR) = 't', FALSE) AS terminated,
    CAST("VECTOR" AS VARCHAR) AS vector,
    CAST("COORDINATE" AS VARCHAR) AS coordinate
FROM "cmhc-34100096"
WHERE "VALUE" IS NOT NULL
