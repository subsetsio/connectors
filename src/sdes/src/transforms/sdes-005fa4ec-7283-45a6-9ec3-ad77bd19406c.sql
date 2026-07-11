-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "VIMP_ENER" AS vimp_ener,
    "VIMP_CMS" AS vimp_cms,
    "VIMP_PETRO" AS vimp_petro,
    "VIMP_BRUT" AS vimp_brut,
    "VIMP_RAFF" AS vimp_raff,
    "VIMP_GAZ" AS vimp_gaz,
    "VIMP_ELE" AS vimp_ele,
    "VEXP_ENER" AS vexp_ener,
    "VEXP_CMS" AS vexp_cms,
    "VEXP_PETRO" AS vexp_petro,
    "VEXP_BRUT" AS vexp_brut,
    "VEXP_RAFF" AS vexp_raff,
    "VEXP_GAZ" AS vexp_gaz,
    "VEXP_ELE" AS vexp_ele,
    "VSOLI_ENER" AS vsoli_ener,
    "VSOLI_CMS" AS vsoli_cms,
    "VSOLI_PETRO" AS vsoli_petro,
    "VSOLI_BRUT" AS vsoli_brut,
    "VSOLI_RAFF" AS vsoli_raff,
    "VSOLI_GAZ" AS vsoli_gaz,
    "VSOLI_ELE" AS vsoli_ele,
    "VSOLI_BIOC" AS vsoli_bioc,
    "VSOLI_BOIS" AS vsoli_bois
FROM "sdes-005fa4ec-7283-45a6-9ec3-ad77bd19406c"
