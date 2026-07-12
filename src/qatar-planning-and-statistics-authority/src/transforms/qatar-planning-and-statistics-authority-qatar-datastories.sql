-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "title",
    "title_ar",
    "theme",
    "theme_ar",
    "type",
    "type_ar",
    "theme_color",
    "img_ar",
    "img",
    "url",
    "description",
    "description_ar"
FROM "qatar-planning-and-statistics-authority-qatar-datastories"
