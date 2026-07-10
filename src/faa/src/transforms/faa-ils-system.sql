-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GLOBAL_ID" AS global_id,
    "REMARKS" AS remarks,
    "ILS_TYPE" AS ils_type,
    "IDENT" AS ident,
    "CAT_CODE" AS cat_code,
    "CHANNEL" AS channel,
    "NAS_USE" AS nas_use,
    "CLASS" AS class,
    "NAME" AS name,
    "CITY" AS city,
    "STATE" AS state,
    "COUNTRY" AS country,
    "AK_LOW" AS ak_low,
    "AK_HIGH" AS ak_high,
    "US_LOW" AS us_low,
    "US_HIGH" AS us_high,
    "US_AREA" AS us_area,
    "PACIFIC" AS pacific
FROM "faa-ils-system"
