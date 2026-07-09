-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains multiple ancillary-service types, regions, and market runs; filter those dimensions before comparing procured, self-provided, total, and cost measures.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "OPR_INTERVAL" AS opr_interval,
    "ANC_TYPE" AS anc_type,
    "ANC_REGION" AS anc_region,
    "GRP" AS grp,
    "MARKET_RUN_ID" AS market_run_id,
    "RESULT_TYPE" AS result_type,
    "UOM" AS uom,
    "POS" AS pos,
    "XML_DATA_ITEM" AS xml_data_item,
    "MW" AS mw,
    "GROUP" AS group
FROM "caiso-as-results"
