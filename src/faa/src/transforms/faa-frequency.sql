-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GLOBAL_ID" AS global_id,
    "REMARKS" AS remarks,
    "FREQ_TRANS" AS freq_trans,
    "FREQ_REC" AS freq_rec,
    "FREQ_UOM" AS freq_uom,
    "TYPE_CODE" AS type_code,
    "SERVICE_ID" AS service_id,
    CAST("FREQ_ALT" AS BIGINT) AS freq_alt,
    "FREQ_USAGE" AS freq_usage,
    "AK_LOW" AS ak_low,
    "AK_HIGH" AS ak_high,
    "US_LOW" AS us_low,
    "US_HIGH" AS us_high,
    "US_AREA" AS us_area,
    "PACIFIC" AS pacific
FROM "faa-frequency"
