-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Overall accountability status rows are categorical designations; count entities rather than summing status text fields.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "overall_status",
    "override",
    "made_progress",
    "made_progress_flag",
    "change_status_flag",
    CAST("institution_id" AS BIGINT) AS institution_id
FROM "new-york-state-education-department-src-accountability-status"
