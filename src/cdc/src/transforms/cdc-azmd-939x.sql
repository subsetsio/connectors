-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State_Tribe_Territory" AS state_tribe_territory,
    "County_Name" AS county_name,
    CAST("FIPS_State" AS BIGINT) AS fips_state,
    CAST("FIPS_County" AS BIGINT) AS fips_county,
    "date",
    "Business_Type" AS business_type,
    "Action" AS action,
    CAST("order_code" AS BIGINT) AS order_code,
    "Source_of_Action" AS source_of_action,
    "URL" AS url,
    "Citation" AS citation,
    "Percent_Capacity_Outdoor" AS percent_capacity_outdoor,
    "Percent_Capacity_Indoor" AS percent_capacity_indoor,
    "Numeric_Capacity_Outdoor" AS numeric_capacity_outdoor,
    "Numeric_Capacity_Indoor" AS numeric_capacity_indoor,
    "Limited_Open_Outdoor_Only" AS limited_open_outdoor_only,
    "Limited_Open_General_Indoor" AS limited_open_general_indoor
FROM "cdc-azmd-939x"
