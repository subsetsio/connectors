-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    "name_ar",
    "type",
    "type_ar",
    "description",
    "description_ar",
    "localisation",
    "empty",
    "date",
    "image",
    "link"
FROM "qatar-planning-and-statistics-authority-event-and-webinars"
