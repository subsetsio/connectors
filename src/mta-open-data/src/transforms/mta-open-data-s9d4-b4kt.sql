-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "agency",
    "job_group_description",
    "eeo_job_category",
    "sex",
    "race_ethnicity",
    "employee_count",
    "new_hires",
    "separations"
FROM "mta-open-data-s9d4-b4kt"
