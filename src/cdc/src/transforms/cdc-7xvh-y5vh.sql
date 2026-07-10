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
    "General_GB_order_group" AS general_gb_order_group,
    CAST("General_GB_order_code" AS BIGINT) AS general_gb_order_code,
    "General_or_Under_6ft_Bans_Gatherings_Over" AS general_or_under_6ft_bans_gatherings_over,
    "Express_Preemption" AS express_preemption,
    "Indoor_Outdoor" AS indoor_outdoor,
    "Source_of_Action" AS source_of_action,
    "URL" AS url,
    "Citation" AS citation
FROM "cdc-7xvh-y5vh"
