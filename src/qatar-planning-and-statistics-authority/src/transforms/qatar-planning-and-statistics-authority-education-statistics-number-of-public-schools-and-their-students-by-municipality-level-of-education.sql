-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality",
    "municipality_ar",
    "level_of_education",
    "level_of_education_ar",
    "type_of_school",
    "type_of_school_ar",
    "number_of_schools",
    "number_of_students",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-public-schools-and-their-students-by-municipality-level-of-education"
