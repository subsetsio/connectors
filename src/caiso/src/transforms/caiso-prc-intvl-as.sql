-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Real-time ancillary-service prices vary by AS type and region; filter those dimensions before comparing prices.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "OPR_TYPE" AS opr_type,
    "ANC_TYPE" AS anc_type,
    "XML_DATA_ITEM" AS xml_data_item,
    "MARKET_RUN_ID" AS market_run_id,
    "MW" AS mw,
    "ANC_REGION" AS anc_region,
    "OPR_INTERVAL" AS opr_interval,
    "GROUP" AS group
FROM "caiso-prc-intvl-as"
