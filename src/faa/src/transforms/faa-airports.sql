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
    "ELEVATION" AS elevation,
    "ICAO_ID" AS icao_id,
    "TYPE_CODE" AS type_code,
    "SERVCITY" AS servcity,
    "STATE" AS state,
    "COUNTRY" AS country,
    "OPERSTATUS" AS operstatus,
    "PRIVATEUSE" AS privateuse,
    "IAPEXISTS" AS iapexists,
    "DODHIFLIP" AS dodhiflip,
    "FAR91" AS far91,
    "FAR93" AS far93,
    "MIL_CODE" AS mil_code,
    "AIRANAL" AS airanal,
    "US_HIGH" AS us_high,
    "US_LOW" AS us_low,
    "AK_HIGH" AS ak_high,
    "AK_LOW" AS ak_low,
    "US_AREA" AS us_area,
    "PACIFIC" AS pacific
FROM "faa-airports"
