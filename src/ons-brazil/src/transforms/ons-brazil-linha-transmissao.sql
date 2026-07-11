-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This registry includes both current and planned transmission-line dates; use the operation and planned-date fields according to the analysis.
SELECT
    "id_subsistema_terminalde",
    "nom_subsistema_terminalde",
    "id_subsistema_terminalpara",
    "nom_subsistema_terminalpara",
    "id_estado_terminalde",
    "nom_estado_de",
    "id_estado_terminalpara",
    "nom_estado_para",
    "nom_subestacao_de",
    "nom_subestacao_para",
    "val_niveltensao_kv",
    "nom_tipoderede",
    "nom_tipolinha",
    "nom_agenteproprietario",
    "nom_linhadetransmissao",
    "cod_equipamento",
    strptime("dat_entradaoperacao", '%Y-%m-%d')::DATE AS dat_entradaoperacao,
    "dat_desativacao",
    "dat_prevista",
    "val_comprimento",
    "val_resistencia",
    "val_reatancia",
    "val_shunt",
    "val_capacoperlongasemlimit",
    "val_capacoperlongacomlimit",
    "val_capacopercurtasemlimit",
    "val_capacopercurtacomlimit",
    "val_capacidadeoperveraodialonga",
    "val_capacidadeoperveraonoitelonga",
    "val_capacoperinvernodialonga",
    "val_capacoperinvernonoitelonga",
    "val_capacoperveradiacurta",
    "val_capacoperveraonoitecurta",
    "val_capacoperinvernodiacurta",
    "val_capacoperinvernonoitecurta",
    "num_barra_de",
    "num_barra_para"
FROM "ons-brazil-linha-transmissao"
