-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "category",
    "value",
    "category_ar"
FROM "qatar-planning-and-statistics-authority-labor-force-participation-rate-lfpr-by-nationality-gender-copy"
