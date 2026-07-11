-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PROD_CMS_SYNT" AS prod_cms_synt,
    "QSOLI_CMS_SYNT" AS qsoli_cms_synt,
    "QIMP_CMS_SYNT" AS qimp_cms_synt,
    "QEXP_CMS_SYNT" AS qexp_cms_synt,
    "VSTO_CMS_SYNT" AS vsto_cms_synt,
    "CI_CMS_SYNT" AS ci_cms_synt,
    "CI_CMS_SYNT_COR1" AS ci_cms_synt_cor1,
    "CI_CMS_SYNT_COR2" AS ci_cms_synt_cor2,
    "DJU" AS dju,
    "INDRIG" AS indrig
FROM "sdes-9862459c-be61-4433-b766-86fcb4c06846"
