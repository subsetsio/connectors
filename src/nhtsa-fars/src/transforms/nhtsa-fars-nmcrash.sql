-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Non-motorist crash-action rows are multi-response observations; do not aggregate as one row per non-motorist.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("PER_NO" AS BIGINT) AS per_no,
    CAST("MTM_CRSH" AS BIGINT) AS mtm_crsh,
    "STATENAME" AS statename,
    "MTM_CRSHNAME" AS mtm_crshname,
    CAST("NMCC" AS BIGINT) AS nmcc,
    "NMCCNAME" AS nmccname,
    "case_year"
FROM "nhtsa-fars-nmcrash"
