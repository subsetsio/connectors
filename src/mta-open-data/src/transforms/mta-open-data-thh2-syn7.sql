-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "borough",
    "minutes_platforms_available",
    "minutes_platforms_in_service",
    "availability",
    "platform_count"
FROM "mta-open-data-thh2-syn7"
