-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "nationality_ar",
    "psychological_and_educational_males",
    "psychological_and_educational_females",
    "social_males",
    "social_females",
    "legal_males",
    "legal_females",
    "shariaa_males",
    "shariaa_females"
FROM "qatar-planning-and-statistics-authority-services-rendered-by-family-consulting-centre-wifaq-through-phone-calls-by-type-of-consultancy-gender-and-nationality"
