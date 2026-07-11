-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Person risk-factor rows are multi-response observations; do not aggregate as one row per person.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    "STATENAME" AS statename,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("PER_NO" AS BIGINT) AS per_no,
    CAST("PERSONRF" AS BIGINT) AS personrf,
    "PERSONRFNAME" AS personrfname,
    "case_year"
FROM "nhtsa-fars-personrf"
