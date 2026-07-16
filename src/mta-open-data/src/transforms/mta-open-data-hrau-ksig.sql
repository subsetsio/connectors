-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "subject",
    "total_complaints",
    "complaints_rate",
    "total_commendations",
    "commendations_rate",
    "ridership"
FROM "mta-open-data-hrau-ksig"
