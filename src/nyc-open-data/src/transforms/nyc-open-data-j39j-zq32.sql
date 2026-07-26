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
    "grades_pk5_enrollment",
    "grades_68_enrollment",
    "grades_912_enrollment",
    "asian",
    "black",
    "hispanic",
    "multiple_race_categories_not_represented",
    "white",
    "swd",
    "ell",
    "poverty",
    "ela_tested",
    "ela_proficient_l34",
    "ela_proficient_l34_1",
    "math_tested",
    "math_proficient_l34",
    "math_proficient_l34_1",
    "total_grad_cohort",
    "_4year_august_graduates" AS 4year_august_graduates,
    "_6year_graduates" AS 6year_graduates
FROM "nyc-open-data-j39j-zq32"
