-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PX_PETRO_FOL_HTS_TONNE" AS px_petro_fol_hts_tonne,
    "PX_PETRO_FOL_BTS_TONNE" AS px_petro_fol_bts_tonne,
    "PX_PETRO_FOL_TBTS_TONNE" AS px_petro_fol_tbts_tonne,
    "PX_PETRO_FOL_HTS_100KWH" AS px_petro_fol_hts_100kwh,
    "PX_PETRO_FOL_BTS_100KWH" AS px_petro_fol_bts_100kwh,
    "PX_PETRO_FOL_TBTS_100KWH" AS px_petro_fol_tbts_100kwh
FROM "sdes-6615e6e2-7150-457a-998f-91e885afc846"
