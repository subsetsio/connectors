-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "question_number",
    "question_text",
    "question_response",
    CAST("total" AS DOUBLE) AS total,
    CAST("regiao_norte" AS DOUBLE) AS regiao_norte,
    CAST("regiao_nordeste" AS DOUBLE) AS regiao_nordeste,
    CAST("regiao_sudeste" AS DOUBLE) AS regiao_sudeste,
    CAST("regiao_sul" AS DOUBLE) AS regiao_sul,
    CAST("regiao_centro" AS DOUBLE) AS regiao_centro,
    CAST("tipo_capital" AS DOUBLE) AS tipo_capital,
    CAST("tipo_rm" AS DOUBLE) AS tipo_rm,
    CAST("tipo_interior" AS DOUBLE) AS tipo_interior,
    CAST("genero_masculino" AS DOUBLE) AS genero_masculino,
    CAST("genero_feminino" AS DOUBLE) AS genero_feminino,
    CAST("idade_16_24" AS DOUBLE) AS idade_16_24,
    CAST("idade_25_34" AS DOUBLE) AS idade_25_34,
    CAST("idade_35_44" AS DOUBLE) AS idade_35_44,
    CAST("idade_45_59" AS DOUBLE) AS idade_45_59,
    CAST("idade_60_mais" AS DOUBLE) AS idade_60_mais,
    CAST("escolaridade__ate_fund_completo" AS DOUBLE) AS escolaridade_ate_fund_completo,
    CAST("escolaridade_medio_completo" AS DOUBLE) AS escolaridade_medio_completo,
    CAST("escolaridade_sup_completo" AS DOUBLE) AS escolaridade_sup_completo,
    CAST("renda_familiar_ate_2_sm" AS DOUBLE) AS renda_familiar_ate_2_sm,
    CAST("renda_familiar_mais_de_2_sm_a_3_sm" AS DOUBLE) AS renda_familiar_mais_de_2_sm_a_3_sm,
    CAST("renda_familiar_mais_de_3_sm_a_5_sm" AS DOUBLE) AS renda_familiar_mais_de_3_sm_a_5_sm,
    CAST("renda_familiar_mais_de_5_sm" AS DOUBLE) AS renda_familiar_mais_de_5_sm,
    CAST("renda_familiar_nao_tem_renda_nao_sabe" AS DOUBLE) AS renda_familiar_nao_tem_renda_nao_sabe,
    CAST("ocupacao_pea" AS DOUBLE) AS ocupacao_pea,
    CAST("ocupacao_nao_pea" AS DOUBLE) AS ocupacao_nao_pea,
    "source_resource"
FROM "idb-data-associated-with-digital-transformation-of-brazilian-governments-citize"
