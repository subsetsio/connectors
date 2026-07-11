-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "region",
    CAST("indeed_job_postings_index" AS DOUBLE) AS indeed_job_postings_index
FROM "indeed-hiring-lab-regional-gb"
