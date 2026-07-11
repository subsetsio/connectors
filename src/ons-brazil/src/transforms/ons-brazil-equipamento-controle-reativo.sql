-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "id_estado",
    "nom_estado",
    "nom_subestacao",
    "nom_agente_proprietario",
    "nom_tipoderede",
    "nom_tipoequipamento",
    "nom_equipamento",
    "val_potreativanominal_mvar",
    "val_limiteinferior_mvar",
    "val_limitesuperior_mvar",
    strptime("dat_entradaoperacao", '%Y-%m-%d')::DATE AS dat_entradaoperacao,
    "dat_desativacao",
    "cod_equipamento"
FROM "ons-brazil-equipamento-controle-reativo"
