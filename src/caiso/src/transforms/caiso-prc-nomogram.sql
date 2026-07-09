-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Nomogram and branch shadow prices vary by constraint and market run; filter those dimensions before aggregating.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "OPR_INTERVAL" AS opr_interval,
    "OPR_TYPE" AS opr_type,
    "MARKET_RUN_ID" AS market_run_id,
    "NOMOGRAM_ID_XML" AS nomogram_id_xml,
    "NOMOGRAM_ID" AS nomogram_id,
    "CONSTRAINT_CAUSE" AS constraint_cause,
    "PRC" AS prc,
    "GROUP" AS group
FROM "caiso-prc-nomogram"
