-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Operating reserve rows are report observations by operating interval; the raw report did not yield a compact scan-verified row key.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DATE" AS opr_date,
    "OPR_INTERVAL" AS opr_interval,
    "OPR_HR" AS opr_hr,
    "MW" AS mw
FROM "caiso-as-op-rsrv"
