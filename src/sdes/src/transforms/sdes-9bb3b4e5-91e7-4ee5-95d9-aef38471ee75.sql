-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PX_GAZ_D_TTES_TRANCHES" AS px_gaz_d_ttes_tranches,
    "PX_GAZ_D_D1" AS px_gaz_d_d1,
    "PX_GAZ_D_D2" AS px_gaz_d_d2,
    "PX_GAZ_D_D3" AS px_gaz_d_d3
FROM "sdes-9bb3b4e5-91e7-4ee5-95d9-aef38471ee75"
