-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The codebook covers only years that ship schema.csv files; older survey response tables have no companion schema rows in this reference table.
-- caution: Column names and question wording are survey-year-specific; use survey_year with column_name when joining to response tables.
SELECT
    "survey_year",
    "column_name",
    "question_text"
FROM "stack-overflow-annual-developer-survey-schema-codebook"
