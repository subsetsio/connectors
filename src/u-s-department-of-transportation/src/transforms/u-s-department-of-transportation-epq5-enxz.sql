-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state_name",
    CAST("number_routes" AS BIGINT) AS number_routes,
    CAST("total_miles" AS DOUBLE) AS total_miles
FROM "u-s-department-of-transportation-epq5-enxz"
