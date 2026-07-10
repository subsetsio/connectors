-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State_Tribe_Territory" AS state_tribe_territory,
    "County_Name" AS county_name,
    "FIPS_Code" AS fips_code,
    strptime("Date", '%Y-%m-%d')::DATE AS date,
    CAST("SAH_Order_Code" AS BIGINT) AS sah_order_code,
    "Stay_at_Home_Order" AS stay_at_home_order,
    "Citations" AS citations
FROM "cdc-hm3s-vk7u"
