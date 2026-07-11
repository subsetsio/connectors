-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Statewide student-growth HEDI data has no district identifier and covers a retired historical evaluation regime.
SELECT
    "report_year",
    CAST("educator_id" AS BIGINT) AS educator_id,
    "role",
    "grade",
    "subject",
    "hedi_rating"
FROM "new-york-state-education-department-spg-state-hedi"
