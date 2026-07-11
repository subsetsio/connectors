-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains both seasonally adjusted and non-seasonally adjusted index columns for each observation; choose the appropriate measure before comparing trends.
SELECT
    "date",
    "jobcountry",
    CAST("indeed_job_postings_index_SA" AS DOUBLE) AS indeed_job_postings_index_sa,
    CAST("indeed_job_postings_index_NSA" AS DOUBLE) AS indeed_job_postings_index_nsa,
    "variable"
FROM "indeed-hiring-lab-aggregate-job-postings"
