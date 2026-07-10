-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State_Tribe_Territory" AS state_tribe_territory,
    "County_Name" AS county_name,
    "FIPS_Code" AS fips_code,
    strptime("Date", '%Y-%m-%d')::DATE AS date,
    CAST("Indoor_GB_Order_Code" AS BIGINT) AS indoor_gb_order_code,
    CAST("General_or_Under_6ft_Bans_Gatherings_Over" AS DOUBLE) AS general_or_under_6ft_bans_gatherings_over,
    "Citations" AS citations
FROM "cdc-3qs9-qnbs"
