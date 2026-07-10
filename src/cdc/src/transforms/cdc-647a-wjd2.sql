-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State_Tribe_Territory" AS state_tribe_territory,
    "County_Name" AS county_name,
    "FIPS_Code" AS fips_code,
    strptime("Date", '%Y-%m-%d')::DATE AS date,
    CAST("Restaurants_Action_Order_Code" AS BIGINT) AS restaurants_action_order_code,
    "Restaurants_Action" AS restaurants_action,
    CAST("Restaurants_Capacity_Outdoor_Percent" AS DOUBLE) AS restaurants_capacity_outdoor_percent,
    CAST("Restaurants_Capacity_Indoor_Percent" AS DOUBLE) AS restaurants_capacity_indoor_percent,
    CAST("Restaurants_Capacity_Outdoor_Number" AS DOUBLE) AS restaurants_capacity_outdoor_number,
    CAST("Restaurants_Capacity_Indoor_Number" AS DOUBLE) AS restaurants_capacity_indoor_number,
    "Citations" AS citations
FROM "cdc-647a-wjd2"
