-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Convergence-bidding reference prices are quarterly node-level values; do not join them to interval price series without aligning the quarter.
SELECT
    "NODE_ID" AS node_id,
    "EFF_QTR_START_DT_GMT" AS eff_qtr_start_dt_gmt,
    "EFF_QTR_END_DT_GMT" AS eff_qtr_end_dt_gmt,
    "EFF_QTR_START_DT" AS eff_qtr_start_dt,
    "EFF_QTR_END_DT" AS eff_qtr_end_dt,
    "SUPPLY_REF_PRICE" AS supply_ref_price,
    "DEMAND_REF_PRICE" AS demand_ref_price,
    "MARKET_RUN_ID" AS market_run_id
FROM "caiso-prc-ds-ref"
