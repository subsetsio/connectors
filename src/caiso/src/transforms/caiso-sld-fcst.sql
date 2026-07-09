-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Demand forecast rows mix forecast horizons, actuals, CAISO total, and TAC areas; filter market_run_id and geography before comparing MW.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "LOAD_TYPE" AS load_type,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "OPR_INTERVAL" AS opr_interval,
    "MARKET_RUN_ID" AS market_run_id,
    "TAC_AREA_NAME" AS tac_area_name,
    "LABEL" AS label,
    "XML_DATA_ITEM" AS xml_data_item,
    "POS" AS pos,
    "MW" AS mw,
    "EXECUTION_TYPE" AS execution_type,
    "GROUP" AS group,
    "LOAD_MW" AS load_mw
FROM "caiso-sld-fcst"
