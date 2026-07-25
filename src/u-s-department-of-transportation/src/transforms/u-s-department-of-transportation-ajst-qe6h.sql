-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    CAST("diesel" AS BIGINT) AS diesel,
    CAST("motor_fuel" AS BIGINT) AS motor_fuel,
    CAST("diesel_1" AS DOUBLE) AS diesel_1
FROM "u-s-department-of-transportation-ajst-qe6h"
