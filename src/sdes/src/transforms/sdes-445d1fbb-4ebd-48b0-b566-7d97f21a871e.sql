-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DEPARTEMENT_CODE" AS departement_code,
    "DEPARTEMENT_LIBELLE" AS departement_libelle,
    "REGION_CODE" AS region_code,
    "REGION_LIBELLE" AS region_libelle,
    "ANNEE" AS annee,
    "CARBUREACTEUR" AS carbureacteur,
    "FOD" AS fod,
    "FOL" AS fol,
    "GAZOLE" AS gazole,
    "GNR" AS gnr,
    "GPL" AS gpl,
    "SUPER_ETH_E85" AS super_eth_e85,
    "SUPER_SANS_PLOMB_95" AS super_sans_plomb_95,
    "SUPER_SANS_PLOMB_95_E10" AS super_sans_plomb_95_e10,
    "SUPER_SANS_PLOMB_98" AS super_sans_plomb_98,
    "SUPER_SANS_PLOMB" AS super_sans_plomb,
    "SUPER_PLOMBE" AS super_plombe
FROM "sdes-445d1fbb-4ebd-48b0-b566-7d97f21a871e"
