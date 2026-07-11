-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("PERIODE", '%Y-%m')::DATE AS periode,
    "PX_PETRO_PROPANE_CITERNE_TONNE" AS px_petro_propane_citerne_tonne,
    "PX_PETRO_PROPANE_CITERNE_100KWH" AS px_petro_propane_citerne_100kwh,
    "PX_PETRO_PROPANE_TONNE" AS px_petro_propane_tonne,
    "PX_PETRO_PROPANE_PCS_100KWH" AS px_petro_propane_pcs_100kwh,
    "PX_PETRO_PROPANE_PCI_100KWH" AS px_petro_propane_pci_100kwh,
    "PX_PETRO_BUTANE_BOUTEILLE13KG" AS px_petro_butane_bouteille13kg,
    "PX_PETRO_FOD_100L_C1" AS px_petro_fod_100l_c1,
    "PX_PETRO_FOD_100KWH_C1" AS px_petro_fod_100kwh_c1,
    "PX_PETRO_ESS_LITRE" AS px_petro_ess_litre,
    "PX_PETRO_SUPER_ARS_LITRE" AS px_petro_super_ars_litre,
    "PX_PETRO_SP95_LITRE" AS px_petro_sp95_litre,
    "PX_PETRO_SP98_LITRE" AS px_petro_sp98_litre,
    "PX_PETRO_GAZOLE_LITRE" AS px_petro_gazole_litre,
    "PX_PETRO_GPLC_LITRE" AS px_petro_gplc_litre,
    "PX_PETRO_SP95_E10_LITRE" AS px_petro_sp95_e10_litre,
    "PX_PETRO_SUPERETHANOL_E85_LITRE" AS px_petro_superethanol_e85_litre
FROM "sdes-daf4715a-0795-4098-bdb1-d90b6e6a568d"
