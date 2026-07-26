-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "site_id",
    "site_name",
    "site_street_address",
    "site_zip_code",
    "site_district",
    "site_borough",
    "class_most_recent_assessment_year",
    "class_emotional_support_score",
    "class_classroom_organization_score",
    "class_instructional_support_score",
    "ecersr_most_recent_assessment_year",
    "ecersr_observation_average_score",
    "ecersr_space_and_furnishings_score",
    "ecersr_personal_care_routines_score",
    "ecersr_language_reasoning_score",
    "ecersr_activities_score",
    "ecersr_interaction_score",
    "ecersr_program_structure_score"
FROM "nyc-open-data-d7da-9deh"
