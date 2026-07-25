-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "port",
    CAST("charleston_sc" AS BIGINT) AS charleston_sc,
    CAST("houston_tx" AS BIGINT) AS houston_tx,
    CAST("long_beach_ca" AS BIGINT) AS long_beach_ca,
    CAST("los_angeles_ca" AS BIGINT) AS los_angeles_ca,
    CAST("nwsa_seattle_tacoma_wa" AS BIGINT) AS nwsa_seattle_tacoma_wa,
    CAST("oakland_ca" AS BIGINT) AS oakland_ca,
    CAST("port_of_ny_nj" AS BIGINT) AS port_of_ny_nj,
    CAST("port_of_virginia_va" AS BIGINT) AS port_of_virginia_va,
    CAST("savannah_ga" AS BIGINT) AS savannah_ga
FROM "u-s-department-of-transportation-rd72-aq8r"
