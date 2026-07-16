-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "time_period",
    "mode",
    "bus_type",
    "question_text",
    "category",
    "measure",
    "score_grain",
    "score_type",
    "score",
    "sample_size"
FROM "mta-open-data-5754-yujh"
