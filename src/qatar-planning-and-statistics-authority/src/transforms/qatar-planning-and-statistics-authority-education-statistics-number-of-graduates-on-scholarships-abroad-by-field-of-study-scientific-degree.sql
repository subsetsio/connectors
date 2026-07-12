-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "field_of_study",
    "field_of_study_ar",
    "doctoral_graduate_males",
    "doctoral_graduate_females",
    "masters_graduate_males",
    "masters_graduate_females",
    "bachelor_graduate_males",
    "bachelor_graduate_females",
    "other_graduate_males",
    "other_graduate_females"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-graduates-on-scholarships-abroad-by-field-of-study-scientific-degree"
