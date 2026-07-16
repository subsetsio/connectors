-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "survey_period_start_date",
    "survey_period_end_date",
    "mode",
    "no_of_observations",
    "mask_worn_correctly",
    "mask_worn_incorrectly",
    "no_mask",
    "total_wearing_a_mask"
FROM "mta-open-data-ijxr-nffj"
