-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Name of Initiative" AS name_of_initiative,
    "Organization Name" AS organization_name,
    "Notes" AS notes,
    "Location 1" AS location_1,
    "Street Address" AS street_address,
    "City" AS city,
    "State" AS state,
    "State Based" AS state_based,
    "Phase 1" AS phase_1,
    "Phase 2" AS phase_2,
    "Facebook" AS facebook,
    "Twitter" AS twitter,
    "Youtube" AS youtube,
    "Website" AS website,
    "Category" AS category,
    "MSA_Name" AS msa_name,
    CAST("Unique ID" AS BIGINT) AS unique_id,
    "Map Display" AS map_display
FROM "cms-44e93e18-b9b3-4650-9471-2b1b31dc588b"
