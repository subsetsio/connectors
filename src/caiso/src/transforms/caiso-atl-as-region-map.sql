-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Effective-dated mapping table; use the effective start and end columns when joining to observations from a specific market date.
SELECT
    "AS_REGION_ID" AS as_region_id,
    "PNODE_ID" AS pnode_id,
    "DESCRIPTION" AS description,
    "COMMENTS" AS comments,
    "EFF_START_DT_GMT" AS eff_start_dt_gmt,
    "EFF_END_DT_GMT" AS eff_end_dt_gmt,
    "EFF_START_DT" AS eff_start_dt,
    "EFF_END_DT" AS eff_end_dt
FROM "caiso-atl-as-region-map"
