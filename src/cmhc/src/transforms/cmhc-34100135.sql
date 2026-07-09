-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: the `geo` column mixes aggregation levels: national, provincial and roll-up rows (e.g. Canada, the provinces, 'Census metropolitan areas', 'All census agglomerations 50,000 and over') appear as ordinary rows alongside individual centres — filter `geo` before summing.
-- caution: `housing_estimates` stacks three distinct measures (housing starts, housing under construction, housing completions) in one value column — starts and completions are flows over the period while under construction is an end-of-period stock; never sum or average across this column.
-- caution: `type_of_unit` mixes subtotals with their components — 'Multiples', 'Total units' overlap the component categories ('Apartment and other unit type', 'Row', 'Semi-detached', 'Single-detached'); summing across the column double-counts. Pick one level.
-- caution: the two `seasonal_adjustment` levels are reported on different scales and bases: 'Unadjusted' rows are counts of units for the month, while 'Seasonally adjusted at annual rates' rows are annualised and expressed in thousands of units. `value` is therefore NOT comparable across this column — filter to one level, and consult `scalar_factor` for the scale that applies to the row.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    "GEO" AS geo,
    "DGUID" AS dguid,
    "Housing estimates" AS housing_estimates,
    "Type of unit" AS type_of_unit,
    "Seasonal adjustment" AS seasonal_adjustment,
    "UOM" AS uom,
    "UOM_ID" AS uom_id,
    "SCALAR_FACTOR" AS scalar_factor,
    "SCALAR_ID" AS scalar_id,
    "VECTOR" AS vector,
    "COORDINATE" AS coordinate,
    "VALUE" AS value,
    "STATUS" AS status,
    "SYMBOL" AS symbol,
    "TERMINATED" AS terminated,
    "DECIMALS" AS decimals
FROM "cmhc-34100135"
