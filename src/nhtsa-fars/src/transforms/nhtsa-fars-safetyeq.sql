-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Non-motorist safety-equipment rows are multi-response observations; do not aggregate as one row per person.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("PER_NO" AS BIGINT) AS per_no,
    CAST("MSAFEQMT" AS BIGINT) AS msafeqmt,
    "STATENAME" AS statename,
    "MSAFEQMTNAME" AS msafeqmtname,
    CAST("NMHELMET" AS BIGINT) AS nmhelmet,
    "NMHELMETNAME" AS nmhelmetname,
    CAST("NMPROPAD" AS BIGINT) AS nmpropad,
    "NMPROPADNAME" AS nmpropadname,
    CAST("NMOTHPRO" AS BIGINT) AS nmothpro,
    "NMOTHPRONAME" AS nmothproname,
    CAST("NMREFCLO" AS BIGINT) AS nmrefclo,
    "NMREFCLONAME" AS nmrefcloname,
    CAST("NMLIGHT" AS BIGINT) AS nmlight,
    "NMLIGHTNAME" AS nmlightname,
    CAST("NMOTHPRE" AS BIGINT) AS nmothpre,
    "NMOTHPRENAME" AS nmothprename,
    "case_year"
FROM "nhtsa-fars-safetyeq"
