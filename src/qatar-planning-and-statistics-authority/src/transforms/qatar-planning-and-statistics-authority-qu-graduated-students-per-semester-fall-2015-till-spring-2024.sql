-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "semester",
    "college",
    "level",
    "major",
    "nationality",
    "gender",
    "number_of_graduates"
FROM "qatar-planning-and-statistics-authority-qu-graduated-students-per-semester-fall-2015-till-spring-2024"
