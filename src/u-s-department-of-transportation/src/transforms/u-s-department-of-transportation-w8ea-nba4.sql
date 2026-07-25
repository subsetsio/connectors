-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    CAST("total_gallons" AS BIGINT) AS total_gallons,
    CAST("total_cost" AS BIGINT) AS total_cost,
    CAST("flight_miles_sm" AS BIGINT) AS flight_miles_sm,
    CAST("flight_miles_flight_sm_gal" AS DOUBLE) AS flight_miles_flight_sm_gal,
    CAST("payload_miles_sm" AS BIGINT) AS payload_miles_sm,
    CAST("payload_miles_payload_sm" AS BIGINT) AS payload_miles_payload_sm
FROM "u-s-department-of-transportation-w8ea-nba4"
