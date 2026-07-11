-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("din_programacaodia", '%Y-%m-%d')::DATE AS din_programacaodia,
    "num_patamar",
    "nom_elementofluxocontrolado",
    "dsc_elementofluxocontrolado",
    "tip_terminal",
    "cod_submercado",
    CAST("val_carga" AS DOUBLE) AS val_carga
FROM "ons-brazil-programacao-fluxo-controlado"
