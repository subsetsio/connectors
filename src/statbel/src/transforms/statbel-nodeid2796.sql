-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "mois",
    "TYPE_ENT_FR" AS type_ent_fr,
    "TYPE_ENT_NL" AS type_ent_nl,
    "NACE1" AS nace1,
    "DESCR_NACE1_FR" AS descr_nace1_fr,
    "DESCR_NACE1_NL" AS descr_nace1_nl,
    "NACE2" AS nace2,
    "DESCR_NACE2_FR" AS descr_nace2_fr,
    "DESCR_NACE2_NL" AS descr_nace2_nl,
    "CD_REGION" AS cd_region,
    "TX_REGION_DESCR_NL" AS tx_region_descr_nl,
    "TX_REGION_DESCR_FR" AS tx_region_descr_fr,
    "REGISTRATIONS_BOP" AS registrations_bop,
    "FIRST_REGISTRATIONS" AS first_registrations,
    "RE_REGISTRATIONS" AS re_registrations,
    "DEREGISTRATIONS" AS deregistrations,
    "EMIGRATIONS" AS emigrations,
    "IMMIGRATIONS" AS immigrations,
    "REGISTRATIONS_EOP" AS registrations_eop
FROM "statbel-nodeid2796"
