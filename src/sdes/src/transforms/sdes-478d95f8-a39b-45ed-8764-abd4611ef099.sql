-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "ACHEM_CODE" AS achem_code,
    "ACHEM_LIBELLE" AS achem_libelle,
    "COND_CODE" AS cond_code,
    "COND_LIBELLE" AS cond_libelle,
    "TONNES" AS tonnes,
    "TKM" AS tkm,
    "UTI_CH" AS uti_ch,
    "UTI_V" AS uti_v,
    "UTI_CH_EVP" AS uti_ch_evp,
    "UTI_V_EVP" AS uti_v_evp
FROM "sdes-478d95f8-a39b-45ed-8764-abd4611ef099"
