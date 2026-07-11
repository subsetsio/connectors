-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DECHET" AS dechet,
    "ANNEE" AS annee,
    "DANGEREUX" AS dangereux,
    "MATIERE_SECHE" AS matiere_seche,
    "NACE_REV2_01_03" AS nace_rev2_01_03,
    "NACE_REV2_04_09" AS nace_rev2_04_09,
    "NACE_REV2_10_12" AS nace_rev2_10_12,
    "NACE_REV2_13_15" AS nace_rev2_13_15,
    "NACE_REV2_16" AS nace_rev2_16,
    "NACE_REV2_17_18" AS nace_rev2_17_18,
    "NACE_REV2_19" AS nace_rev2_19,
    "NACE_REV2_20_22" AS nace_rev2_20_22,
    "NACE_REV2_23" AS nace_rev2_23,
    "NACE_REV2_24_25" AS nace_rev2_24_25,
    "NACE_REV2_26_30" AS nace_rev2_26_30,
    "NACE_REV2_31_33" AS nace_rev2_31_33,
    "NACE_REV2_34_35" AS nace_rev2_34_35,
    "NACE_REV2_36ET37ET39" AS nace_rev2_36et37et39,
    "NACE_REV2_38" AS nace_rev2_38,
    "NACE_REV2_41_43" AS nace_rev2_41_43,
    "NACE_REV2_GUSAUF4677" AS nace_rev2_gusauf4677,
    "NACE_REV2_4677" AS nace_rev2_4677,
    "NACE_REV2_HH" AS nace_rev2_hh,
    "NACE_REV2_TOTAL" AS nace_rev2_total
FROM "sdes-4ffeb0da-dec8-45c8-aab6-363738a997dc"
