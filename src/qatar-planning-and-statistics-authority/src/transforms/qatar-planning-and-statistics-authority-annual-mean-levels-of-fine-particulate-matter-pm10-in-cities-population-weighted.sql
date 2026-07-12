-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "aspire_zone",
    "aspire_zone_ar",
    "qatar_university",
    "qatar_university_ar",
    "corniche",
    "corniche_ar"
FROM "qatar-planning-and-statistics-authority-annual-mean-levels-of-fine-particulate-matter-pm10-in-cities-population-weighted"
