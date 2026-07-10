-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "mes",
    "id_municipio",
    "regiao_ssp",
    "homicidio_doloso",
    "numero_de_vitimas_em_homicidio_doloso",
    "homicidio_doloso_por_acidente_de_transito",
    "numero_de_vitimas_em_homicidio_doloso_por_acidente_de_transito",
    "homicidio_culposo_por_acidente_de_transito",
    "homicidio_culposo_outros",
    "tentativa_de_homicidio",
    "lesao_corporal_seguida_de_morte",
    "lesao_corporal_dolosa",
    "lesao_corporal_culposa_por_acidente_de_transito",
    "lesao_corporal_culposa_outras",
    "latrocinio",
    "numero_de_vitimas_em_latrocinio",
    "total_de_estupro",
    "estupro",
    "estupro_de_vulneravel",
    "total_de_roubo_outros",
    "roubo_outros",
    "roubo_de_veiculo",
    "roubo_a_banco",
    "roubo_de_carga",
    "furto_outros",
    "furto_de_veiculo"
FROM "base-dos-dados-br-sp-gov-ssp--ocorrencias-registradas"
