-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Renewable forecasts vary by market run, trading hub, and renewable type; filter those dimensions before summing MW.
SELECT
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "OPR_INTERVAL" AS opr_interval,
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "TRADING_HUB" AS trading_hub,
    "RENEWABLE_TYPE" AS renewable_type,
    "LABEL" AS label,
    "XML_DATA_ITEM" AS xml_data_item,
    "MARKET_RUN_ID_POS" AS market_run_id_pos,
    "RENEW_POS" AS renew_pos,
    "MW" AS mw,
    "MARKET_RUN_ID" AS market_run_id,
    "GROUP" AS group
FROM "caiso-sld-ren-fcst"
