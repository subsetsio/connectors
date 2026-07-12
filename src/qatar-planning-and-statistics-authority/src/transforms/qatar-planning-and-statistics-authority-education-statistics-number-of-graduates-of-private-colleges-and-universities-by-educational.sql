-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "educational_institution",
    "educational_institution_arabic",
    "qataris_male",
    "qataris_female",
    "non_qataris_male",
    "non_qataris_female"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-graduates-of-private-colleges-and-universities-by-educational"
