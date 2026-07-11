-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are subgroup accountability designations and may overlap across subgroup populations.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "school_type",
    "subgroup_name",
    "overall_status",
    "made_progress",
    "override",
    "made_progress_flag",
    "change_status_flag",
    "change_progress_flag",
    "institution_id"
FROM "new-york-state-education-department-src-accountability-status-by-subgroup"
