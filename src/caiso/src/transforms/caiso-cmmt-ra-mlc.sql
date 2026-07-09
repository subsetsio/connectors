-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains commitment capacity, minimum-load MW, and cost observations by market run and operating interval; filter the commitment dimensions before summing.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "MARKET_RUN_ID" AS market_run_id,
    "RA_MLC_TYPE" AS ra_mlc_type,
    "UOM" AS uom,
    "XML_DATA_ITEM" AS xml_data_item,
    "MW" AS mw,
    "GROUP" AS group
FROM "caiso-cmmt-ra-mlc"
