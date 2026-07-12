-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_services",
    "type_of_services_ar",
    "qatari_male_child",
    "qatari_female_child",
    "qatari_women",
    "non_qatari_male_child",
    "non_qatari_female_child",
    "non_qatari_women"
FROM "qatar-planning-and-statistics-authority-services-provided-to-cases-received-by-the-protection-and-social-rehabilitation-center-aman-by-nationality-gender-and-service-type"
