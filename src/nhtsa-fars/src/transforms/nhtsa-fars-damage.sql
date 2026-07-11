-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Vehicle damage and impact rows are multi-response observations; do not aggregate as one row per vehicle.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("MDAREAS" AS BIGINT) AS mdareas,
    "STATENAME" AS statename,
    "MDAREASNAME" AS mdareasname,
    CAST("DAMAGE" AS BIGINT) AS damage,
    "DAMAGENAME" AS damagename,
    "case_year"
FROM "nhtsa-fars-damage"
