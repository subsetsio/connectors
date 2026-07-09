-- Statistics Canada table 34-10-0135 (CMHC).
-- Faithful pass-through of the raw asset: renames, casts, and a filter that drops
-- rows with no observation (StatCan suppresses them via STATUS, leaving VALUE null).
-- caution: the `geo` column mixes aggregation levels: national, provincial and roll-up rows (e.g. Canada, the provinces, 'Census metropolitan areas', 'All census agglomerations 50,000 and over') appear as ordinary rows alongside individual centres — filter `geo` before summing.
-- caution: `housing_estimates` stacks three distinct measures (housing starts, housing under construction, housing completions) in one value column — starts and completions are flows over the period while under construction is an end-of-period stock; never sum or average across this column.
-- caution: `type_of_unit` mixes subtotals with their components — 'Multiples', 'Total units' overlap the component categories ('Apartment and other unit type', 'Row', 'Semi-detached', 'Single-detached'); summing across the column double-counts. Pick one level.
-- caution: the two `seasonal_adjustment` levels are reported on different scales and bases: 'Unadjusted' rows are counts of dwelling units for the quarter, while 'Seasonally adjusted at annual rates' rows are annualised and expressed in thousands of units. `value` is therefore NOT comparable across this column — filter to one level, and read `scalar_factor` for the scale that applies to the row.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    CAST("GEO" AS VARCHAR) AS geo,
    CAST("DGUID" AS VARCHAR) AS dguid,
    CAST("Housing estimates" AS VARCHAR) AS housing_estimates,
    CAST("Type of unit" AS VARCHAR) AS type_of_unit,
    CAST("Seasonal adjustment" AS VARCHAR) AS seasonal_adjustment,
    CAST("VALUE" AS DOUBLE) AS value,
    TRIM(CAST("SCALAR_FACTOR" AS VARCHAR)) AS scalar_factor,
    COALESCE(CAST("TERMINATED" AS VARCHAR) = 't', FALSE) AS terminated,
    CAST("VECTOR" AS VARCHAR) AS vector,
    CAST("COORDINATE" AS VARCHAR) AS coordinate
FROM "cmhc-34100135"
WHERE "VALUE" IS NOT NULL
