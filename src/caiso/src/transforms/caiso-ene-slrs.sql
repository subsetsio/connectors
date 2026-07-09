-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: System load and resource schedules mix CAISO total, TAC areas, schedules, and market runs; filter geography, schedule, and market run before aggregating MW.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "SLRS_TYPE" AS slrs_type,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "OPR_INTERVAL" AS opr_interval,
    "MARKET_RUN_ID" AS market_run_id,
    "TAC_ZONE_NAME" AS tac_zone_name,
    "SCHEDULE" AS schedule,
    "XML_DATA_ITEM" AS xml_data_item,
    "POS" AS pos,
    "MW" AS mw,
    "GROUP" AS group
FROM "caiso-ene-slrs"
