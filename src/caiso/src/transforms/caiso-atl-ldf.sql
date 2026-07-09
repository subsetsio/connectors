-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Load distribution factors are effective-dated mappings between APNodes and PNodes; join using the applicable effective period.
SELECT
    "EFF_START_DT_GMT" AS eff_start_dt_gmt,
    "EFF_END_DT_GMT" AS eff_end_dt_gmt,
    "EFF_START_DT" AS eff_start_dt,
    "EFF_END_DT" AS eff_end_dt,
    "APNODE_ID" AS apnode_id,
    "PNODE_ID" AS pnode_id,
    "DIST_FACTOR" AS dist_factor,
    "SEASON" AS season,
    "TIME_OF_USE" AS time_of_use,
    "DESCRIPTION" AS description,
    "COMMENTS" AS comments,
    "GROUP" AS group
FROM "caiso-atl-ldf"
