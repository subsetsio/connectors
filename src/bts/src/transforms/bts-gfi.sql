-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CARRIER" AS carrier,
    "CARRIER_ENTITY" AS carrier_entity,
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH" AS BIGINT) AS month,
    "EXPENSE_TYPE" AS expense_type,
    CAST("EXP_FLIGHT_ATTENDANTS" AS DOUBLE) AS exp_flight_attendants,
    CAST("EXP_TRAFFIC" AS DOUBLE) AS exp_traffic,
    CAST("EXP_DEPARTURE_STATION" AS DOUBLE) AS exp_departure_station,
    CAST("EXP_CAPACITY_ADMIN" AS DOUBLE) AS exp_capacity_admin,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-gfi"
