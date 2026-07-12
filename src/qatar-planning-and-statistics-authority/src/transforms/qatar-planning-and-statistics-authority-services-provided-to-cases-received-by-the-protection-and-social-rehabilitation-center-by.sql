-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_services",
    "type_of_services_ar",
    "nationality",
    "nationality_ar",
    "age_group",
    "age_group_ar",
    "gender",
    "gender_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-services-provided-to-cases-received-by-the-protection-and-social-rehabilitation-center-by"
