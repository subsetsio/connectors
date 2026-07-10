-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "GRD_FIXID" AS grd_fixid,
    "GRD_FLOAID" AS grd_floaid,
    "GRD_NEWID" AS grd_newid,
    "SHAPE_Leng" AS shape_leng,
    "SHAPE_Area" AS shape_area,
    CAST("TOT_P" AS BIGINT) AS tot_p,
    CAST("TOT_F" AS BIGINT) AS tot_f,
    CAST("TOT_M" AS BIGINT) AS tot_m
FROM "statbel-nodeid593"
