-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Average class size rows can carry both wide subject columns and class_description/value columns depending on source year; compare the same class dimension.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "common_branch",
    "grade_8_math",
    "grade_8_english",
    "grade_8_sci",
    "grade_8_ss",
    "grade_10_english",
    "grade_10_math",
    "grade_10_sci",
    "grade_10_ss",
    "class_description",
    "average_class_size",
    "data_reported"
FROM "new-york-state-education-department-studed-average-class-size"
