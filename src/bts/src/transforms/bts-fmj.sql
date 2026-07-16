-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PILOTEXPENSE" AS pilotexpense,
    "AIRCRAFT_FUEL" AS aircraft_fuel,
    "OTHER_EXPENSES" AS other_expenses,
    "TOTAL_DIRECT_LESS_RENT" AS total_direct_less_rent,
    "MAINTENANCE" AS maintenance,
    "DEPAND_RENTAL" AS depand_rental,
    "TOTAL_DIRECT" AS total_direct,
    "FLIGHT_ATTENDANTS" AS flight_attendants,
    "TRAFFIC" AS traffic,
    "DEPARTURE" AS departure,
    "CAPACITY" AS capacity,
    "TOTAL_INDIRECT" AS total_indirect,
    "TOTAL_OP_EXPENSE" AS total_op_expense,
    "TOTAL_AIR_HOURS" AS total_air_hours,
    "AIR_DAYS_ASSIGN" AS air_days_assign,
    "AIR_FUELS_ISSUED" AS air_fuels_issued,
    CAST("AIRCRAFT_CONFIG" AS BIGINT) AS aircraft_config,
    CAST("AIRCRAFT_GROUP" AS BIGINT) AS aircraft_group,
    CAST("AIRCRAFT_TYPE" AS BIGINT) AS aircraft_type,
    CAST("AIRLINE_ID" AS BIGINT) AS airline_id,
    "UNIQUE_CARRIER" AS unique_carrier,
    "UNIQUE_CARRIER_NAME" AS unique_carrier_name,
    "CARRIER" AS carrier,
    "CARRIER_NAME" AS carrier_name,
    "UNIQUE_CARRIER_ENTITY" AS unique_carrier_entity,
    "REGION" AS region,
    CAST("CARRIER_GROUP_NEW" AS BIGINT) AS carrier_group_new,
    CAST("CARRIER_GROUP" AS BIGINT) AS carrier_group,
    CAST("YEAR" AS BIGINT) AS year,
    CAST("QUARTER" AS BIGINT) AS quarter,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-fmj"
