-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GLOBAL_ID" AS global_id,
    "IDENT" AS ident,
    "NAME" AS name,
    "LATITUDE" AS latitude,
    "LONGITUDE" AS longitude,
    "WKHR_CODE" AS wkhr_code,
    "WKHR_RMK" AS wkhr_rmk,
    "ELEVATION" AS elevation,
    "FREQUENCY" AS frequency,
    "MAGVAR" AS magvar,
    CAST("MAGVAR_DAT" AS BIGINT) AS magvar_dat,
    "NAV_TYPE" AS nav_type,
    "TYPE_CODE" AS type_code,
    "NAVSYS_ID" AS navsys_id,
    "AWYSTRUC" AS awystruc,
    "CHANNEL" AS channel,
    "STATUS" AS status,
    "VOICE" AS voice,
    "SLAVEVAR" AS slavevar,
    CAST("PRIVATE" AS BIGINT) AS private,
    "AK_LOW" AS ak_low,
    "AK_HIGH" AS ak_high,
    "US_LOW" AS us_low,
    "US_HIGH" AS us_high,
    "US_AREA" AS us_area,
    "PACIFIC" AS pacific
FROM "faa-navaid-component"
