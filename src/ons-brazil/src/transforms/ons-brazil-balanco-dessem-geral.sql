-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verified row identity includes measured values because the source does not expose a stable program interval identifier.
SELECT
    strptime("din_programacaodia", '%Y-%m-%d')::DATE AS din_programacaodia,
    "num_patamar",
    "cod_subsistema",
    CAST("val_demanda" AS DOUBLE) AS val_demanda,
    CAST("val_geracao_renovavel" AS DOUBLE) AS val_geracao_renovavel,
    CAST("val_geracao_hidraulica" AS DOUBLE) AS val_geracao_hidraulica,
    CAST("val_geracao_termica" AS DOUBLE) AS val_geracao_termica,
    CAST("val_cons_elevatoria" AS DOUBLE) AS val_cons_elevatoria
FROM "ons-brazil-balanco-dessem-geral"
