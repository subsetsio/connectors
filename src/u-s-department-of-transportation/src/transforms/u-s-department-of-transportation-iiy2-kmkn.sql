-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("date" AS TIMESTAMP) AS date,
    CAST("all_u_s_container_ports" AS BIGINT) AS all_u_s_container_ports,
    CAST("los_angeles_long_beach" AS BIGINT) AS los_angeles_long_beach,
    CAST("savannah" AS BIGINT) AS savannah,
    CAST("all_other_ports" AS BIGINT) AS all_other_ports
FROM "u-s-department-of-transportation-iiy2-kmkn"
