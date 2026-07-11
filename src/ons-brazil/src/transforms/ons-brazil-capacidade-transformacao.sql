-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "id_estado",
    "nom_estado",
    "nom_tipotransformador",
    "nom_agenteproprietario",
    "nom_subestacao",
    "nom_transformador",
    "cod_equipamento",
    strptime("dat_entradaoperacao", '%Y-%m-%d')::DATE AS dat_entradaoperacao,
    "dat_desativacao",
    "val_tensaoprimario_kv",
    "val_tensaosecundario_kv",
    "val_tensaoterciario_kv",
    "val_potencianominal_mva",
    "nom_tipoderede",
    "num_barra_primario",
    "num_barra_secundario"
FROM "ons-brazil-capacidade-transformacao"
