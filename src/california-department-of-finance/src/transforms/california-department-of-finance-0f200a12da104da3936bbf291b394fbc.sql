-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Yearv1" AS BIGINT) AS yearv1,
    "County" AS county,
    "COUNTY_SORT" AS county_sort,
    "SF_HU" AS sf_hu,
    "MHU_HU" AS mhu_hu,
    "MF_HU" AS mf_hu,
    "SUM_HU" AS sum_hu,
    "ObjectId" AS objectid
FROM "california-department-of-finance-0f200a12da104da3936bbf291b394fbc"
