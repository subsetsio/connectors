-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State_Tribe_Territory" AS state_tribe_territory,
    "County_Name" AS county_name,
    "FIPS_Code" AS fips_code,
    strptime("Date", '%Y-%m-%d')::DATE AS date,
    CAST("Bars_Action_Order_Code" AS BIGINT) AS bars_action_order_code,
    "Bars_Action" AS bars_action,
    CAST("Bars_Capacity_Outdoor_Percent" AS DOUBLE) AS bars_capacity_outdoor_percent,
    CAST("Bars_Capacity_Indoor_Percent" AS DOUBLE) AS bars_capacity_indoor_percent,
    CAST("Bars_Capacity_Outdoor_Number" AS DOUBLE) AS bars_capacity_outdoor_number,
    CAST("Bars_Capacity_Indoor_Number" AS DOUBLE) AS bars_capacity_indoor_number,
    "Citations" AS citations,
    "unique_id"
FROM "cdc-kp49-9dp8"
