-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "semester",
    "college",
    "level",
    "major",
    "nationality",
    "gender",
    "total_registered"
FROM "qatar-planning-and-statistics-authority-qu-registered-students-per-semester-fall-2015-till-spring-2025"
