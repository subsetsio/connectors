-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State_Tribe_Territory" AS state_tribe_territory,
    "County_Name" AS county_name,
    "FIPS_Code" AS fips_code,
    strptime("Date", '%Y-%m-%d')::DATE AS date,
    CAST("Masks_Order_Code" AS BIGINT) AS masks_order_code,
    "Face_Masks_Required_in_Public" AS face_masks_required_in_public,
    "Citations" AS citations
FROM "cdc-42jj-z7fa"
