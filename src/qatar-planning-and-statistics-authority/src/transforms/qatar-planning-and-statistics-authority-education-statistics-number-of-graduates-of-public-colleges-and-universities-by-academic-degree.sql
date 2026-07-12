-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "academic_degree",
    "academic_degree_ar",
    "academic_program",
    "academic_program_ar",
    "educational_institution",
    "educational_institution_ar",
    "qataris_males",
    "qataris_females",
    "non_qataris_males",
    "non_qataris_females"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-graduates-of-public-colleges-and-universities-by-academic-degree"
