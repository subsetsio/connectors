-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "ontrack_year1_2013",
    "graduation_rate_2013",
    "college_career_rate_2013",
    "student_satisfaction_2013",
    "ontrack_year1_2012",
    "graduation_rate_2012",
    "college_career_rate_2012",
    "student_satisfaction_2012",
    "ontrack_year1_historic_avg_similar_schls",
    "graduation_rate_historic_avg_similar_schls",
    "college_career_rate_historic_avg_similar_schls",
    "student_satisfaction_historic_avg_similar_schls",
    "quality_review_rating",
    "quality_review_year"
FROM "nyc-open-data-xahu-rkwn"
