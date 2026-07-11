-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "REG_CODE" AS reg_code,
    "REG_LIBELLE" AS reg_libelle,
    "DEP_CODE" AS dep_code,
    "DEP_LIBELLE" AS dep_libelle,
    "COMM" AS comm,
    "NUM_PD" AS num_pd,
    "ETAT_PD" AS etat_pd,
    "DATE_REELLE_AUTORISATION" AS date_reelle_autorisation,
    "AN_DEPOT" AS an_depot,
    "DR_DEPOT" AS dr_depot,
    strptime("DPC_AUT", '%Y-%m')::DATE AS dpc_aut,
    "DPC_DERN" AS dpc_dern,
    "APE_DEM" AS ape_dem,
    "CJ_DEM" AS cj_dem,
    "DENOM_DEM" AS denom_dem,
    "SIREN_DEM" AS siren_dem,
    "SIRET_DEM" AS siret_dem,
    "CODPOST_DEM" AS codpost_dem,
    "LOCALITE_DEM" AS localite_dem,
    "REC_ARCHI" AS rec_archi,
    "ADR_NUM_TER" AS adr_num_ter,
    "ADR_LIBVOIE_TER" AS adr_libvoie_ter,
    "ADR_LIEUDIT_TER" AS adr_lieudit_ter,
    "ADR_LOCALITE_TER" AS adr_localite_ter,
    "ADR_CODPOST_TER" AS adr_codpost_ter,
    "SEC_CADASTRE1" AS sec_cadastre1,
    "NUM_CADASTRE1" AS num_cadastre1,
    "SEC_CADASTRE2" AS sec_cadastre2,
    "NUM_CADASTRE2" AS num_cadastre2,
    "SEC_CADASTRE3" AS sec_cadastre3,
    "NUM_CADASTRE3" AS num_cadastre3,
    "SUPERFICIE_TERRAIN" AS superficie_terrain,
    "ZONE_OP" AS zone_op
FROM "sdes-1a9a2f0c-56fe-4e69-84a7-fbbda2121f02"
