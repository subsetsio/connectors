-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "subject_code",
    "successor_subject_code",
    "union_date",
    "subject_name_act",
    "subject_name_hist",
    "succ_subject_name_act",
    "succ_subject_name_hist",
    "deputy_subject_name",
    "succ_deputy_subject_name",
    "grp_parent_name",
    "grp_name"
FROM "national-bank-of-slovakia-dsw-subject-union"
