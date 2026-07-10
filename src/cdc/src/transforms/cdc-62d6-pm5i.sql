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
    CAST("order_code" AS BIGINT) AS order_code,
    "Face_Masks_Required_in_Public" AS face_masks_required_in_public,
    "Source_of_Action" AS source_of_action,
    "URL" AS url,
    "Citation" AS citation
FROM "cdc-62d6-pm5i"
