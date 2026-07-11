-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an effective-dated name and grouping history. Join on subject codes and validity ranges when reconstructing a reporting-period view.
SELECT
    "deputy_subject_code",
    "deputy_subject_name",
    "subject_code",
    "subject_name_act",
    "subject_name_hist",
    "name_from",
    "name_till",
    "valid_from",
    "valid_till",
    "grp_parent_name",
    "grp_name",
    "in_grp_from",
    "in_grp_till"
FROM "national-bank-of-slovakia-dsw-subject-history"
