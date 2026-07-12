-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_group",
    "age_group_ar",
    "nationality",
    "nationality_ar",
    "type_of_service",
    "type_of_service_ar",
    "gender",
    "gender_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-services-rendered-in-social-rehabilitation-center-owain-by-service-type-age-group-nationality-and"
