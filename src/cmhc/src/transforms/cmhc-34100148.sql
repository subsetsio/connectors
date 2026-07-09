-- Statistics Canada table 34-10-0148 (CMHC).
-- Faithful pass-through of the raw asset: renames, casts, and a filter that drops
-- rows with no observation (StatCan suppresses them via STATUS, leaving VALUE null).
-- caution: the `geo` column mixes aggregation levels: national, provincial and roll-up rows (e.g. Canada, the provinces, 'Census metropolitan areas', 'All census agglomerations 50,000 and over') appear as ordinary rows alongside individual centres — filter `geo` before summing.
-- caution: `type_of_dwelling_unit` mixes subtotals with their components — 'Total units' overlap the component categories ('Apartment and other types of units', 'Row units', 'Semi-detached units', 'Single units'); summing across the column double-counts. Pick one level.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    CAST("GEO" AS VARCHAR) AS geo,
    CAST("DGUID" AS VARCHAR) AS dguid,
    CAST("Type of dwelling unit" AS VARCHAR) AS type_of_dwelling_unit,
    CAST("Type of market" AS VARCHAR) AS type_of_market,
    CAST("VALUE" AS DOUBLE) AS value,
    COALESCE(CAST("TERMINATED" AS VARCHAR) = 't', FALSE) AS terminated,
    CAST("VECTOR" AS VARCHAR) AS vector,
    CAST("COORDINATE" AS VARCHAR) AS coordinate
FROM "cmhc-34100148"
WHERE "VALUE" IS NOT NULL
