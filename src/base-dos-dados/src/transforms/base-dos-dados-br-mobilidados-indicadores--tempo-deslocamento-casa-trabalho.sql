-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "sigla_uf",
    "id_municipio",
    "tempo_medio_deslocamento",
    "prop_deslocamento_acima_1_hora"
FROM "base-dos-dados-br-mobilidados-indicadores--tempo-deslocamento-casa-trabalho"
