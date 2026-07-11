-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PROD_CMS" AS prod_cms,
    "QIMP_CMS" AS qimp_cms,
    "QEXP_CMS" AS qexp_cms,
    "VSTO_CMS" AS vsto_cms,
    "CI_CMS" AS ci_cms,
    "CPE_CMS" AS cpe_cms,
    "CAT_CMS" AS cat_cms,
    "CSID_CMS" AS csid_cms,
    "LIND_CMS" AS lind_cms,
    "LRT_CMS" AS lrt_cms,
    "CI_CMS_COR1" AS ci_cms_cor1,
    "CPE_CMS_COR1" AS cpe_cms_cor1,
    "CSID_CMS_COR1" AS csid_cms_cor1,
    "CI_CMS_COR2" AS ci_cms_cor2,
    "CPE_CMS_COR2" AS cpe_cms_cor2,
    "CSID_CMS_COR2" AS csid_cms_cor2,
    "ST_CMS" AS st_cms,
    "DJU" AS dju,
    "INDRIG" AS indrig
FROM "sdes-e555e02d-6a6b-408e-8129-173d38dbdc5c"
