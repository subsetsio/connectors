-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GLOBAL_ID" AS global_id,
    "AIRPORT_ID" AS airport_id,
    "DESIGNATOR" AS designator,
    "LENGTH" AS length,
    "WIDTH" AS width,
    "DIM_UOM" AS dim_uom,
    "COMP_CODE" AS comp_code,
    "LIGHTACTV" AS lightactv,
    "LIGHTINTNS" AS lightintns,
    "AK_LOW" AS ak_low,
    "AK_HIGH" AS ak_high,
    "US_LOW" AS us_low,
    "US_HIGH" AS us_high,
    "US_AREA" AS us_area,
    "PACIFIC" AS pacific,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "faa-runways"
