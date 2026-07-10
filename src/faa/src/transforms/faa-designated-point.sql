-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GLOBAL_ID" AS global_id,
    "REMARKS" AS remarks,
    "IDENT" AS ident,
    "LATITUDE" AS latitude,
    "LONGITUDE" AS longitude,
    "NOTES_ID" AS notes_id,
    "MIL_CODE" AS mil_code,
    "TYPE_CODE" AS type_code,
    "REPATC" AS repatc,
    "MAGVAR" AS magvar,
    "MAGVAR_DT" AS magvar_dt,
    "ONSHORE" AS onshore,
    "STRUCTURE" AS structure,
    "REFFAC" AS reffac,
    "MRA_VAL" AS mra_val,
    "MRA_UOM" AS mra_uom,
    "STATE" AS state,
    "COUNTRY" AS country,
    "AK_LOW" AS ak_low,
    "AK_HIGH" AS ak_high,
    "US_LOW" AS us_low,
    "US_HIGH" AS us_high,
    "US_AREA" AS us_area,
    "PACIFIC" AS pacific
FROM "faa-designated-point"
