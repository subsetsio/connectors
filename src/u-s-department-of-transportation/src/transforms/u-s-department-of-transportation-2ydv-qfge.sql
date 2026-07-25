-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("rank" AS BIGINT) AS rank,
    "airport",
    CAST("enplaned_passengers" AS BIGINT) AS enplaned_passengers,
    CAST("year" AS BIGINT) AS year,
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude
FROM "u-s-department-of-transportation-2ydv-qfge"
