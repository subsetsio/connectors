-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: the `geo` column mixes aggregation levels: national, provincial and roll-up rows (e.g. Canada, the provinces, 'Census metropolitan areas', 'All census agglomerations 50,000 and over') appear as ordinary rows alongside individual centres — filter `geo` before summing.
-- caution: `housing_estimates` stacks three distinct measures (housing starts, housing under construction, housing completions) in one value column — starts and completions are flows over the period while under construction is an end-of-period stock; never sum or average across this column.
-- caution: `type_of_unit` mixes subtotals with their components — 'Total units' overlap the component categories ('Apartment and other units', 'Row units', 'Semi-detached units', 'Single-detached units'); summing across the column double-counts. Pick one level.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    "GEO" AS geo,
    "DGUID" AS dguid,
    "Housing estimates" AS housing_estimates,
    "Type of unit" AS type_of_unit,
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
FROM "cmhc-34100151"
