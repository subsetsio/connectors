-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PX_GAZ_I_TRANCHES_I1_I5" AS px_gaz_i_tranches_i1_i5,
    "PX_GAZ_I_I1" AS px_gaz_i_i1,
    "PX_GAZ_I_I2" AS px_gaz_i_i2,
    "PX_GAZ_I_I3" AS px_gaz_i_i3,
    "PX_GAZ_I_I4" AS px_gaz_i_i4,
    "PX_GAZ_I_I5" AS px_gaz_i_i5,
    "PX_GAZ_I_I6" AS px_gaz_i_i6,
    "PX_GAZ_I_TTES_TRANCHES" AS px_gaz_i_ttes_tranches
FROM "sdes-04be4886-e771-4c76-8b7a-cdd10a30aef2"
