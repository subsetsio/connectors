-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "MARKET_RUN_ID" AS market_run_id,
    "NODE_ID" AS node_id,
    "XML_DATA_ITEM" AS xml_data_item,
    "MW" AS mw,
    "GROUP" AS group
FROM "caiso-ene-cb-clr-awards"
