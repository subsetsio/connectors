-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "jobcountry",
    CAST("indeed_job_postings_index" AS DOUBLE) AS indeed_job_postings_index,
    "variable",
    "display_name"
FROM "indeed-hiring-lab-job-postings-by-sector"
