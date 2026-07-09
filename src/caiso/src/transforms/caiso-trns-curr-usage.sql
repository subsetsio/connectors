-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Current transmission usage is continuously updated and varies by interface and direction; use the interval timestamp to select the applicable snapshot.
SELECT
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "TI_ID" AS ti_id,
    "TI_DIRECTION" AS ti_direction,
    "MARKET_RUN_ID" AS market_run_id,
    "TI_CONSTRAINT_ID" AS ti_constraint_id,
    "TR_TYPE" AS tr_type,
    "XML_DATA_ITEM" AS xml_data_item,
    "LABEL" AS label,
    "POS" AS pos,
    "OPR_INTERVAL" AS opr_interval,
    "MW" AS mw,
    "GROUP" AS group
FROM "caiso-trns-curr-usage"
