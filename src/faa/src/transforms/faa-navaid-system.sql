-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GLOBAL_ID" AS global_id,
    "TYPE_CODE" AS type_code,
    "IDENT" AS ident,
    "CHANNEL" AS channel,
    "NAS_USE" AS nas_use,
    "CLASS_TXT" AS class_txt,
    "NAME_TXT" AS name_txt,
    "CITY" AS city,
    "STATE" AS state,
    "COUNTRY" AS country,
    "STATUS" AS status,
    "REMARKS" AS remarks,
    "AK_LOW" AS ak_low,
    "AK_HIGH" AS ak_high,
    "US_LOW" AS us_low,
    "US_HIGH" AS us_high,
    "US_AREA" AS us_area,
    "PACIFIC" AS pacific
FROM "faa-navaid-system"
