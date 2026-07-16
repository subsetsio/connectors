-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "date",
    "area",
    "year",
    "month",
    "daily_vmt_agps",
    "daily_vmt_cvd",
    "indexed_average_vmt"
FROM "mta-open-data-jbxx-kxff"
