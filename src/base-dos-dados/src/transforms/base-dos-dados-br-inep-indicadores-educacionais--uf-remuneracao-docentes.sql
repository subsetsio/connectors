-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "sigla_uf",
    "rede",
    "escolaridade",
    "numero_docentes",
    "prop_docentes_rais",
    "rem_bruta_rais_1_quartil",
    "rem_bruta_rais_mediana",
    "rem_bruta_rais_media",
    "rem_bruta_rais_3_quartil",
    "rem_bruta_rais_desvio_padrao",
    "carga_horaria_media_semanal",
    "rem_media_40_horas_semanais"
FROM "base-dos-dados-br-inep-indicadores-educacionais--uf-remuneracao-docentes"
