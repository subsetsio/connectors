-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "project_id",
    "phase",
    "phase_sequence",
    "phase_state",
    "phase_est_actual_start_date",
    "phase_est_actual_end_date",
    "activity_title",
    "activity_description",
    "activity_date",
    "activity_flag",
    "url",
    "update_date"
FROM "mta-open-data-nswv-d6bz"
