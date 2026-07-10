-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_deputado",
    "cpf",
    "nome_civil",
    "nome_civil_upper",
    "sexo",
    "municipio_nascimento",
    "estado_abrev_nascimento",
    strptime("data_nascimento", '%Y-%m-%d')::DATE AS data_nascimento,
    "escolaridade",
    "escolaridade_nova",
    "ultimo_status_nome",
    "ultimo_status_nome_eleitoral",
    "sigla_partido_original",
    "sigla_partido",
    "estado_abrev",
    CAST("ultimo_status_data" AS TIMESTAMP) AS ultimo_status_data,
    "ultima_legislatura",
    "ultimo_status_condicao_eleitoral",
    "ultimo_status_situacao",
    "gabinete_predio",
    "gabinete_andar",
    "gabinete_sala",
    "gabinete_telefone",
    "email",
    "gabinete_nome",
    "url_partido",
    "url_foto",
    CAST("capture_date" AS TIMESTAMP) AS capture_date,
    "api_url"
FROM "base-dos-dados-br-camara-atividade-legislativa--deputados"
