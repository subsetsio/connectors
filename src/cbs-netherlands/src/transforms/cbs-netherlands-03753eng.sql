-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TypeOfEducation" AS typeofeducation,
    "IdeologicalBasisOfTheSchool" AS ideologicalbasisoftheschool,
    "Schoolsize" AS schoolsize,
    "Periods" AS periods,
    "SchoolsInstitutions_1" AS schoolsinstitutions_1,
    "EnrolledPupilsStudents_2" AS enrolledpupilsstudents_2,
    "TypeOfEducation_label" AS typeofeducation_label,
    "IdeologicalBasisOfTheSchool_label" AS ideologicalbasisoftheschool_label,
    "Schoolsize_label" AS schoolsize_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-03753eng"
