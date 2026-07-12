-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "nationality",
    "gender",
    "municipality",
    "number_of_people_with_difficulties",
    "lbldy",
    "lnw",
    "ljnsy",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-special-needs-statistics-number-of-people-with-disabilities-by-nationality-gender-and-municipality"
