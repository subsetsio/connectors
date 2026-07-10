-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Awardee" AS awardee,
    "Awardee State" AS awardee_state,
    "Enhanced Prenatal Care Approaches" AS enhanced_prenatal_care_approaches,
    "Location of the Enhanced Prenatal Care Services" AS location_of_the_enhanced_prenatal_care_services,
    CAST("Award Amount (Year 1)" AS BIGINT) AS award_amount_year_1
FROM "cms-9d4218d7-bb48-4278-964b-01755f0d8a85"
