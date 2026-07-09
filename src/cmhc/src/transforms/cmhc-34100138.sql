-- Statistics Canada table 34-10-0138 (CMHC).
-- Faithful pass-through of the raw asset: renames, casts, and a filter that drops
-- rows with no observation (StatCan suppresses them via STATUS, leaving VALUE null).
-- caution: `housing_estimates` stacks three distinct measures (housing starts, housing under construction, housing completions) in one value column — starts and completions are flows over the period while under construction is an end-of-period stock; never sum or average across this column.
-- caution: `type_of_unit` mixes subtotals with their components — 'Total units' overlap the component categories ('Apartment and other units', 'Row units', 'Semi-detached units', 'Single-detached units'); summing across the column double-counts. Pick one level.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    CAST("GEO" AS VARCHAR) AS geo,
    CAST("DGUID" AS VARCHAR) AS dguid,
    CAST("Housing estimates" AS VARCHAR) AS housing_estimates,
    CAST("Type of unit" AS VARCHAR) AS type_of_unit,
    CAST("VALUE" AS DOUBLE) AS value,
    COALESCE(CAST("TERMINATED" AS VARCHAR) = 't', FALSE) AS terminated,
    CAST("VECTOR" AS VARCHAR) AS vector,
    CAST("COORDINATE" AS VARCHAR) AS coordinate
FROM "cmhc-34100138"
WHERE "VALUE" IS NOT NULL
