-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide job postings table; columns encode industry and wage/occupation slices, so compare like-named measures rather than summing across all bg_posts* columns.
SELECT
    "year",
    "month",
    "day_endofweek",
    "bg_posts",
    "bg_posts_ss30",
    "bg_posts_ss55",
    "bg_posts_ss60",
    "bg_posts_ss65",
    "bg_posts_ss70",
    "bg_posts_jz1",
    "bg_posts_jzgrp12",
    "bg_posts_jz2",
    "bg_posts_jz3",
    "bg_posts_jzgrp345",
    "bg_posts_jz4",
    "bg_posts_jz5"
FROM "opportunity-insights-tracker-job-postings-national-weekly"
