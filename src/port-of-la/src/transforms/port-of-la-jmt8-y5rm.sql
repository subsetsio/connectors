-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("ship_calls" AS BIGINT) AS ship_calls,
    CAST("passengers" AS BIGINT) AS passengers,
    CAST("passengers_per_ship" AS BIGINT) AS passengers_per_ship
FROM "port-of-la-jmt8-y5rm"
