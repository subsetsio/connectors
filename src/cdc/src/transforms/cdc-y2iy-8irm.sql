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
    CAST("Order_code" AS BIGINT) AS order_code,
    "Stay_at_Home_Order_Recommendation" AS stay_at_home_order_recommendation,
    "Express_Preemption" AS express_preemption,
    "Source_of_Action" AS source_of_action,
    "URL" AS url,
    "Citation" AS citation
FROM "cdc-y2iy-8irm"
