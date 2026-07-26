-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "ontrack_year1_2013",
    "graduation_rate_2013",
    "college_career_rate_2013",
    "ontrack_year1_2014",
    "graduation_rate_2014",
    "college_career_rate_2014",
    "ontrack_year1_boro",
    "graduation_rate_boro",
    "college_career_rate_boro",
    "pct_stu_enough_variety_2014",
    "pct_stu_safe_2014",
    "quality_review_year",
    "qr_curriculum",
    "qr_instruction",
    "qr_assessing_student_learning",
    "qr_high_expectations",
    "qr_teacher_collaboration"
FROM "nyc-open-data-qvir-knu3"
