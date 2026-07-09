-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Marginal-loss rows include multiple market runs and value types; filter those dimensions before comparing dollars and MWh.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "OPR_INTERVAL" AS opr_interval,
    "MARKET_RUN_ID" AS market_run_id,
    "LOSS_TYPE" AS loss_type,
    "XML_DATA_ITEM" AS xml_data_item,
    "UOM" AS uom,
    "VALUE" AS value,
    "GROUP" AS group
FROM "caiso-ene-loss"
