-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("unnamed_column" AS TIMESTAMP) AS unnamed_column,
    CAST("charleston" AS BIGINT) AS charleston,
    CAST("houston" AS BIGINT) AS houston,
    CAST("long_beach" AS BIGINT) AS long_beach,
    CAST("los_angeles" AS BIGINT) AS los_angeles,
    CAST("ny_nj" AS BIGINT) AS ny_nj,
    CAST("oakland" AS BIGINT) AS oakland,
    CAST("port_of_va" AS BIGINT) AS port_of_va,
    CAST("savannah" AS BIGINT) AS savannah,
    CAST("sea_tac" AS BIGINT) AS sea_tac,
    CAST("total" AS BIGINT) AS total
FROM "u-s-department-of-transportation-iahn-a7j4"
