-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Day-ahead market summary rows mix physical and virtual demand, supply, import, and export quantities; filter the category columns before aggregating totals.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "MARKET_RUN_ID" AS market_run_id,
    "PRODUCT_TYPE" AS product_type,
    "PRODUCT_TYPE_ORDER" AS product_type_order,
    "SUMMARY_CAT" AS summary_cat,
    "SUMMARY_CAT_ORDER" AS summary_cat_order,
    "SELF_SCHEDULE" AS self_schedule,
    "ENERGY_BID" AS energy_bid,
    "VIRTUAL_BID" AS virtual_bid,
    "TOTAL" AS total,
    "GROUP" AS group
FROM "caiso-ene-cb-mkt-sum"
