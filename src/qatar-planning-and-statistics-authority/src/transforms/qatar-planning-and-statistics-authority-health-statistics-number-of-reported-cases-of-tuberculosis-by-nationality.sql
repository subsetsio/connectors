-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "bangladeshi",
    "egyptian",
    "filipino",
    "indian",
    "iranian",
    "nepali",
    "pakistani",
    "qatari",
    "saudi",
    "somali",
    "other"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-reported-cases-of-tuberculosis-by-nationality"
