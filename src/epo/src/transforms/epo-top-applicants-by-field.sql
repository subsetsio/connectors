-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a latest-edition ranking snapshot, not a historical time series.
SELECT
    CAST("field_id" AS BIGINT) AS field_id,
    CAST("edition_year" AS BIGINT) AS edition_year,
    "rank",
    "applicant_name",
    CAST("number_of_applications" AS BIGINT) AS number_of_applications
FROM "epo-top-applicants-by-field"
