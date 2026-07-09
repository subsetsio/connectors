-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Real-time flowgate shadow prices vary by interface and direction; filter those dimensions before aggregating.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "OPR_INTERVAL" AS opr_interval,
    "TI_ID" AS ti_id,
    "TI_DIRECTION" AS ti_direction,
    "MARKET_RUN_ID" AS market_run_id,
    "CONSTRAINT_CAUSE" AS constraint_cause,
    "PRC" AS prc,
    "GROUP" AS group
FROM "caiso-prc-rtm-flowgate"
