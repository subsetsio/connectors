-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "id_estado",
    "nom_estado",
    "nom_modalidadeoperacao",
    "nom_agenteproprietario",
    "nom_agenteoperador",
    "nom_tipousina",
    "nom_usina",
    "ceg",
    "nom_unidadegeradora",
    "cod_equipamento",
    "num_unidadegeradora",
    "nom_combustivel",
    "dat_entradateste",
    strptime("dat_entradaoperacao", '%Y-%m-%d')::DATE AS dat_entradaoperacao,
    "dat_desativacao",
    "val_potenciaefetiva"
FROM "ons-brazil-capacidade-geracao"
