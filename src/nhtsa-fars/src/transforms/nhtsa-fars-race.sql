-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Race rows can contain multiple race codes per person; do not aggregate as one row per person.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    "STATENAME" AS statename,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("PER_NO" AS BIGINT) AS per_no,
    CAST("RACE" AS BIGINT) AS race,
    "RACENAME" AS racename,
    CAST("ORDER" AS BIGINT) AS order,
    CAST("MULTRACE" AS BIGINT) AS multrace,
    "ORDERNAME" AS ordername,
    "MULTRACENAME" AS multracename,
    "case_year"
FROM "nhtsa-fars-race"
