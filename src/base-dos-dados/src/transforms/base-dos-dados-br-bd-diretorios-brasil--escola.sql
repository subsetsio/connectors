-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_escola",
    "nome",
    "id_municipio",
    "sigla_uf",
    "restricao_atendimento",
    "localizacao",
    "localidade_diferenciada",
    "categoria_administrativa",
    "endereco",
    "telefone",
    "dependencia_administrativa",
    "categoria_privada",
    "conveniada_poder_publico",
    "regulacao_conselho_educacao",
    "porte",
    "etapas_modalidades_oferecidas",
    "outras_ofertas_educacionais",
    "latitude",
    "longitude"
FROM "base-dos-dados-br-bd-diretorios-brasil--escola"
