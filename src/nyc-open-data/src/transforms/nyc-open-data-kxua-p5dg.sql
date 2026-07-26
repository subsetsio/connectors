-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "unnamed_column",
    "counseling_services",
    "counseling_services_bilingual",
    "speechlanguage_therapy",
    "speechlanguage_therapy_bilingual",
    "occupational_therapy",
    "physical_therapy",
    "hearing_education_services",
    "vision_education_services",
    "all_services"
FROM "nyc-open-data-kxua-p5dg"
