-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Graduation outcome counts are subgroup aggregates; avoid adding overlapping subgroup rows together.
SELECT
    "report_year",
    "school_year",
    CAST("institution_id" AS BIGINT) AS institution_id,
    "entity_cd",
    "entity_name",
    CAST("membership_code" AS BIGINT) AS membership_code,
    "membership_desc",
    "subgroup_name",
    "total_enrolled",
    "num_grad",
    "per_grad",
    "num_regents_adv_desig",
    "per_regents_adv_desig",
    "num_regents_diploma",
    "per_regents_diploma",
    "num_local_diploma",
    "per_local_diploma",
    "num_non_diploma_cred",
    "per_non_diploma_cred",
    "num_still_enrolled",
    "per_still_enrolled",
    "num_ged_transfer",
    "per_ged_transfer",
    "num_dropout",
    "per_dropout"
FROM "new-york-state-education-department-ell-graduation-rate"
