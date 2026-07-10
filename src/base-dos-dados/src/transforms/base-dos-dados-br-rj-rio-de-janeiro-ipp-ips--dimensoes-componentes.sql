-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "regiao_administrativa",
    "ips_geral",
    "necessidades_humanas_basicas_nota_dimensao",
    "nutricao_cuidados_medicos_basicos",
    "agua_saneamento",
    "moradia",
    "seguranca_pessoal",
    "fundamentos_bem_estar_nota_dimensao",
    "acesso_conhecimento_basico",
    "acesso_informacao",
    "saude_bem_estar",
    "qualidade_meio_ambiente",
    "oportunidades_nota_dimensao",
    "direitos_individuais",
    "liberdades_individuais",
    "tolerancia_inclusao",
    "acesso_educacao_superior"
FROM "base-dos-dados-br-rj-rio-de-janeiro-ipp-ips--dimensoes-componentes"
