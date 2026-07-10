-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Yearv1" AS yearv1,
    "County" AS county,
    "COUNTYv1" AS countyv1,
    "SF_HU" AS sf_hu,
    "MHU_HU" AS mhu_hu,
    "MF_HU" AS mf_hu,
    "SUM_HU" AS sum_hu,
    "ObjectId" AS objectid
FROM "california-department-of-finance-603566ca1e3041c699fe924a12dc6f1b"
