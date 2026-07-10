-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sequencial_sessao",
    strptime("data_sessao", '%Y-%m-%d')::DATE AS data_sessao,
    "sigla_partido",
    "sigla_uf_partido",
    "bloco_parlamentar",
    "nome_discursante",
    "genero_discursante",
    "categoria_discursante",
    "texto_discurso",
    "horario_inicio_discurso",
    "horario_fim_discurso",
    "duracao_discurso",
    "sinalizacao_pela_ordem",
    "sinalizacao_questao_ordem",
    "sinalizacao_fora_microfone",
    "sinalizacao_responder_questao_ordem",
    "sinalizacao_por_videoconferencia",
    "sinalizacao_para_interpelar",
    "sinalizacao_para_expor",
    "sinalizacao_para_depor",
    "sinalizacao_como_presidente"
FROM "base-dos-dados-br-senado-cpipandemia--discursos"
