-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "PEAK_FLAG" AS peak_flag,
    "GROUP" AS group
FROM "caiso-atl-peak-on-off"
