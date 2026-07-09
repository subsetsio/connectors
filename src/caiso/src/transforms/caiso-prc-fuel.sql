-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Fuel prices vary by fuel region; filter fuel region before comparing daily gas prices.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "FUEL_REGION_ID_XML" AS fuel_region_id_xml,
    "FUEL_REGION_ID" AS fuel_region_id,
    "PRC" AS prc,
    "GROUP" AS group
FROM "caiso-prc-fuel"
