-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_deputado",
    "nome",
    "aniversario",
    "sigla_partido",
    "situacao",
    "email",
    "sala",
    "placa_veiculo",
    "home_page",
    "andar",
    "matricula",
    "id_spl"
FROM "base-dos-dados-br-sp-alesp--deputado"
