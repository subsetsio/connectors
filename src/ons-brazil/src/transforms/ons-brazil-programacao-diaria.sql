-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "din_programacaodia",
    "num_patamar",
    "cod_exibicaousina",
    "nom_usina",
    "tip_geracao",
    "nom_modalidadeoperacao",
    "id_subsistema",
    "nom_subsistema",
    "id_estado",
    "nom_estado",
    CAST("val_geracaoprogramada" AS DOUBLE) AS val_geracaoprogramada,
    "val_disponibilidade",
    "val_ordemmerito",
    "val_inflexibilidade",
    "val_uc",
    "val_razaoeletrica",
    "val_geracaoenergetica",
    "val_gesubgsub",
    "val_exportacao",
    "val_reposicaoexportacao",
    "val_faltacombustivel"
FROM "ons-brazil-programacao-diaria"
