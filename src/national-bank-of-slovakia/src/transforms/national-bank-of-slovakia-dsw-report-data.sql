-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are reported values by supervised subject, value type, currency, and reporting period, but the source does not expose a verified row identifier; avoid assuming uniqueness when aggregating.
-- caution: The table carries both current and historical subject/group labels. Use the subject history reference table when effective-dated names or group membership matter.
SELECT
    "period",
    "subject_code",
    "val_type",
    "currency",
    "num_value",
    "subject_name_act",
    "subject_name_hist",
    "deputy_subject_code",
    "deputy_subject_name",
    "grp_name",
    "grp_parent_name"
FROM "national-bank-of-slovakia-dsw-report-data"
