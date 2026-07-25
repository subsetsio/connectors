-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("date" AS TIMESTAMP) AS date,
    CAST("cincinnati_rate" AS DOUBLE) AS cincinnati_rate,
    CAST("rate" AS DOUBLE) AS rate,
    CAST("st_louis_rate" AS DOUBLE) AS st_louis_rate,
    CAST("rate_1" AS DOUBLE) AS rate_1,
    CAST("cairo_memphis_rate" AS DOUBLE) AS cairo_memphis_rate,
    CAST("rate_3" AS DOUBLE) AS rate_3
FROM "u-s-department-of-transportation-t48m-82hq"
