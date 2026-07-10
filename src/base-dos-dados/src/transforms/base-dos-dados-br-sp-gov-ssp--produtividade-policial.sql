-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "id_municipio",
    "regiao_ssp",
    "ocorrencias_de_porte_de_entorpecentes",
    "ocorrencias_de_trafico_de_entorpecentes",
    "ocorrencias_de_apreensao_de_entorpecentes",
    "ocorrencias_de_porte_ilegal_de_arma",
    "numero_de_armas_de_fogo_apreendidas",
    "numero_de_flagrantes_lavrados",
    "numero_de_infratores_apreendidos_em_flagrante",
    "numero_de_infratores_apreendidos_por_mandado",
    "numero_de_pessoas_presas_em_flagrante",
    "numero_de_pessoas_presas_por_mandado",
    "numero_de_prisoes_efetuadas",
    "numero_de_veiculos_recuperados",
    "total_de_inqueritos_policiais_instaurados"
FROM "base-dos-dados-br-sp-gov-ssp--produtividade-policial"
