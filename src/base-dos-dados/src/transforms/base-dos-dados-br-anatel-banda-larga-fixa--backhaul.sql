-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sigla_uf",
    "id_municipio",
    "situacao",
    "ano_atendimento",
    "concessionaria",
    "tecnologia",
    "capacidade_backhaul",
    "capacidade_ocupada",
    "capacidade_disponivel"
FROM "base-dos-dados-br-anatel-banda-larga-fixa--backhaul"
