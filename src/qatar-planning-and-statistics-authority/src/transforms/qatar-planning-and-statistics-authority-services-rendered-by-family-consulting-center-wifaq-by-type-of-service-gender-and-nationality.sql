-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality_ar",
    "nationality",
    "psychological_and_educational_males",
    "psychological_and_educational_females",
    "social_males",
    "social_females",
    "legal_males",
    "legal_females",
    "shariaa_males",
    "shariaa_females"
FROM "qatar-planning-and-statistics-authority-services-rendered-by-family-consulting-center-wifaq-by-type-of-service-gender-and-nationality"
