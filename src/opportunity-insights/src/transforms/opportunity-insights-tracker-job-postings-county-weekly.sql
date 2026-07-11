-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "day_endofweek",
    "countyfips",
    "bg_posts",
    "bg_posts_jzgrp12",
    "bg_posts_jzgrp345"
FROM "opportunity-insights-tracker-job-postings-county-weekly"
