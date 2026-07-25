-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("population" AS BIGINT) AS population,
    CAST("drivers" AS BIGINT) AS drivers,
    CAST("vehicles" AS BIGINT) AS vehicles
FROM "u-s-department-of-transportation-9hnm-fr6r"
