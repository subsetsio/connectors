-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Demand forecast rows mix forecast horizons, actuals, CAISO total, and TAC areas; filter market_run_id and geography before comparing MW.
SELECT
    src."INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    src."INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    src."LOAD_TYPE" AS load_type,
    src."OPR_DT" AS opr_dt,
    src."OPR_HR" AS opr_hr,
    src."OPR_INTERVAL" AS opr_interval,
    src."MARKET_RUN_ID" AS market_run_id,
    src."TAC_AREA_NAME" AS tac_area_name,
    src."LABEL" AS label,
    src."XML_DATA_ITEM" AS xml_data_item,
    src."POS" AS pos,
    src."MW" AS mw,
    src."EXECUTION_TYPE" AS execution_type,
    src."GROUP" AS group,
    src."LOAD_MW" AS load_mw
FROM "caiso-sld-fcst" AS src
