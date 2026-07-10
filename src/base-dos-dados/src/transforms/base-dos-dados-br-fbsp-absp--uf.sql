-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "sigla_uf",
    "quantidade_cvli",
    "quantidade_feminicidio",
    "quantidade_ocorrencia_homicidio_doloso",
    "quantidade_vitima_homicidio_doloso",
    "quantidade_latrocinio",
    "quantidade_lesao_corporal_seguida_de_morte",
    "quantidade_morte_a_esclarecer",
    "quantidade_morte_intervencao_policial_civil_servico",
    "quantidade_morte_intervencao_policial_civil_fora_servico",
    "quantidade_morte_intervencao_policial_militar_servico",
    "quantidade_morte_intervencao_policial_militar_fora_servico",
    "quantidade_morte_violenta_intencional",
    "quantidade_policial_civil_morto_confronto_servico",
    "quantidade_policial_civil_morto_confronto_fora_servico",
    "quantidade_policial_militar_morto_confronto_servico",
    "quantidade_policial_militar_morto_confronto_fora_servico",
    "quantidade_suicidio",
    "quantidade_estupro",
    "quantidade_tentativa_estupro",
    "quantidade_furto_veiculo",
    "quantidade_roubo_instituicao_financeira",
    "quantidade_roubo_carga",
    "quantidade_roubo_de_veiculo",
    "quantidade_arma_fogo_apreendida",
    "quantidade_registro_pessoa_desaparecida",
    "quantidade_populacao_sistema_penitenciario",
    "despesa_empenhada_seguranca_publica"
FROM "base-dos-dados-br-fbsp-absp--uf"
