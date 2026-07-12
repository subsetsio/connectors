-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_service",
    "type_of_service_ar",
    "gender",
    "gender_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-services-provided-to-cases-received-by-naufar-center-by-gender-and-service-type"
