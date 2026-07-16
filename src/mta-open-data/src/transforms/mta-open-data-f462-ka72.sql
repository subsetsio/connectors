-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "open_dataset_id",
    "dataset_title",
    "type",
    "agency",
    "posting_frequency",
    "description",
    "status",
    "dataset_created_at",
    "plan_submission_date",
    "nys_url",
    "plan_submission_date_notes"
FROM "mta-open-data-f462-ka72"
