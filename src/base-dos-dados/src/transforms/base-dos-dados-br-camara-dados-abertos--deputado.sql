-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nome",
    "nome_civil",
    strptime("data_nascimento", '%Y-%m-%d')::DATE AS data_nascimento,
    strptime("data_falecimento", '%Y-%m-%d')::DATE AS data_falecimento,
    "id_municipio_nascimento",
    "sigla_uf_nascimento",
    "id_deputado",
    "sexo",
    "id_inicial_legislatura",
    "id_final_legislatura",
    "url_site",
    "url_rede_social"
FROM "base-dos-dados-br-camara-dados-abertos--deputado"
