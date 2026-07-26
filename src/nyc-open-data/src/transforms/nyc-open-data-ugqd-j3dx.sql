-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "district",
    "school_name",
    "is_org_splitsited",
    "building_ids",
    "transfer_school",
    "total_enrollment",
    "grades_3k5_enrollment",
    "grades_68_enrollment",
    "grades_912_enrollment",
    "asian",
    "black",
    "hispanic",
    "multiracial",
    "native_american",
    "white",
    "missing_raceethnicity_data",
    "swd",
    "ell",
    "poverty",
    "_201819_ela_tested" AS 201819_ela_tested,
    "_201819_ela_proficient_l34" AS 201819_ela_proficient_l34,
    "_201819_ela_proficient_l34_1" AS 201819_ela_proficient_l34_1,
    "_201819_math_tested" AS 201819_math_tested,
    "_201819_math_proficient_l34" AS 201819_math_proficient_l34,
    "_201819_math_proficient_l34_1" AS 201819_math_proficient_l34_1,
    "_201920_total_4year_august_grad_cohort" AS 201920_total_4year_august_grad_cohort,
    "_201920_4year_august_graduates" AS 201920_4year_august_graduates,
    "_201920_total_6year_grad_cohort" AS 201920_total_6year_grad_cohort,
    "_201920_6year_graduates" AS 201920_6year_graduates
FROM "nyc-open-data-ugqd-j3dx"
