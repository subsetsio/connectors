-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "sigla_uf",
    "id_municipio",
    "cnae_2_secao",
    "cnae_2_subclasse",
    "saldo_movimentacao",
    "cbo_2002",
    "categoria",
    "grau_instrucao",
    "idade",
    "horas_contratuais",
    "raca_cor",
    "sexo",
    "tipo_empregador",
    "tipo_estabelecimento",
    "tipo_movimentacao",
    "tipo_deficiencia",
    "indicador_trabalho_intermitente",
    "indicador_trabalho_parcial",
    "salario_mensal",
    "tamanho_estabelecimento_janeiro",
    "indicador_aprendiz",
    "origem_informacao",
    "indicador_exclusao",
    "indicador_fora_prazo"
FROM "base-dos-dados-br-me-caged--microdados-movimentacao-excluida"
