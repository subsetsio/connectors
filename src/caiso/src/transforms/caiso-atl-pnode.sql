-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PNODE_ID" AS pnode_id,
    "PNODE_TYPE" AS pnode_type,
    "DESCRIPTION" AS description,
    "COMMENTS" AS comments,
    "EFF_START_DT" AS eff_start_dt,
    "EFF_END_DT" AS eff_end_dt,
    "EFF_START_DT_GMT" AS eff_start_dt_gmt,
    "EFF_END_DT_GMT" AS eff_end_dt_gmt,
    "CB_NODE_FLAG" AS cb_node_flag,
    "MAX_CB_MW" AS max_cb_mw,
    "MAX_CB_MW_EFF_START_DT" AS max_cb_mw_eff_start_dt,
    "MAX_CB_MW_EFF_END_DT" AS max_cb_mw_eff_end_dt,
    "MAX_CB_MW_EFF_START_DT_GMT" AS max_cb_mw_eff_start_dt_gmt,
    "MAX_CB_MW_EFF_END_DT_GMT" AS max_cb_mw_eff_end_dt_gmt
FROM "caiso-atl-pnode"
