-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "target_group",
    "target_group_ar",
    "gender",
    "gender_ar",
    "type_of_services",
    "type_of_services_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-assistance-provided-by-qatar-foundation-for-child-and-woman-by-type-of-service"
