-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Peak forecast rows mix CAISO total and TAC-area geography; filter the geography before aggregating load.
SELECT
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "TAC_AREA_NAME" AS tac_area_name,
    "LOAD_MW" AS load_mw,
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt
FROM "caiso-sld-fcst-peak"
