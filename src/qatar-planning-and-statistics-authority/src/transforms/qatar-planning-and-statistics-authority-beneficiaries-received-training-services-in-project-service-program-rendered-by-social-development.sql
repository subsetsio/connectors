-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "nationality_ar",
    "gender",
    "gender_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-beneficiaries-received-training-services-in-project-service-program-rendered-by-social-development"
