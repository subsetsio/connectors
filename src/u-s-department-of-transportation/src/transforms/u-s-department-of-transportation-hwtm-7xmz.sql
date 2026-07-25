-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    CAST("auto" AS BIGINT) AS auto,
    CAST("bus" AS BIGINT) AS bus,
    CAST("truck" AS BIGINT) AS truck,
    CAST("motorcycle" AS BIGINT) AS motorcycle
FROM "u-s-department-of-transportation-hwtm-7xmz"
