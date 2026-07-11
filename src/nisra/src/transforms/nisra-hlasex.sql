-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Academic year" AS academic_year,
    "SEX" AS sex,
    "Sex Label" AS sex_label,
    "FEHE" AS fehe,
    "Further education / Higher education" AS further_education_higher_education,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-hlasex"
