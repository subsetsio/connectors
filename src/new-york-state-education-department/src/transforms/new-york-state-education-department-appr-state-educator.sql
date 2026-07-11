-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Statewide APPR researcher data has no district identifier and covers the former 2012-13 through 2015-16 evaluation regime.
SELECT
    "report_year",
    CAST("educator_id" AS BIGINT) AS educator_id,
    "role",
    "grade",
    "subject",
    "overall_composite_score",
    "overall_composite_rating",
    "growth_rating",
    "local_hedi",
    "other_rating"
FROM "new-york-state-education-department-appr-state-educator"
