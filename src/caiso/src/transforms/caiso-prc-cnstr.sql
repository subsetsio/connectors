-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Constraint shadow prices vary by market run and interface or constraint identifier; filter those dimensions before aggregating.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "OPR_INTERVAL" AS opr_interval,
    "OPR_TYPE" AS opr_type,
    "MARKET_RUN_ID" AS market_run_id,
    "TI_ID_XML" AS ti_id_xml,
    "TI_ID" AS ti_id,
    "TI_DIRECTION" AS ti_direction,
    "CONSTRAINT_CAUSE" AS constraint_cause,
    "MW" AS mw,
    "GROUP" AS group
FROM "caiso-prc-cnstr"
