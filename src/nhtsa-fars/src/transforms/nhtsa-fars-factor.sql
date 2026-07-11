-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Vehicle factor rows are multi-response observations; do not aggregate as one row per vehicle.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("MFACTOR" AS BIGINT) AS mfactor,
    "STATENAME" AS statename,
    "MFACTORNAME" AS mfactorname,
    CAST("VEHICLECC" AS BIGINT) AS vehiclecc,
    "VEHICLECCNAME" AS vehicleccname,
    "case_year"
FROM "nhtsa-fars-factor"
