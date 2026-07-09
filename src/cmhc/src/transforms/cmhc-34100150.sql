-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: the `geo` column mixes aggregation levels: national, provincial and roll-up rows (e.g. Canada, the provinces, 'Census metropolitan areas', 'All census agglomerations 50,000 and over') appear as ordinary rows alongside individual centres — filter `geo` before summing.
-- caution: `completed_dwelling_units` stacks a flow (absorptions during the period) and a stock (unabsorbed inventory at period end) in one value column — never sum across this column.
-- caution: `type_of_dwelling_unit` mixes subtotals with their components — 'Total units' overlap the component categories ('Semi-detached units', 'Single detached units'); summing across the column double-counts. Pick one level.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    "GEO" AS geo,
    "DGUID" AS dguid,
    "Completed dwelling units" AS completed_dwelling_units,
    "Type of dwelling unit" AS type_of_dwelling_unit,
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
FROM "cmhc-34100150"
