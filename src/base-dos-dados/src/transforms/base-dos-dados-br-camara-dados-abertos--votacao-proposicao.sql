-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_votacao",
    strptime("data", '%Y-%m-%d')::DATE AS data,
    "descricao",
    "id_proposicao",
    "ano_proposicao",
    "titulo",
    "ementa",
    "codigo_tipo",
    "sigla_tipo",
    "numero"
FROM "base-dos-dados-br-camara-dados-abertos--votacao-proposicao"
