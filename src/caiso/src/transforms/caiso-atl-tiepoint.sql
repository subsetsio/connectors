-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TI_ID" AS ti_id,
    "TIEPOINT_ID" AS tiepoint_id,
    "TSIN" AS tsin,
    "DESCRIPTION" AS description,
    "COMMENTS" AS comments,
    "EFF_START_DT_GMT" AS eff_start_dt_gmt,
    "EFF_END_DT_GMT" AS eff_end_dt_gmt,
    "EFF_START_DT" AS eff_start_dt,
    "EFF_END_DT" AS eff_end_dt
FROM "caiso-atl-tiepoint"
