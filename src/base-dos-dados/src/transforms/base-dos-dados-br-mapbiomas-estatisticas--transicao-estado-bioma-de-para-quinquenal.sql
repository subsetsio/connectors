-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "sigla_uf",
    "bioma",
    "de_id_classe",
    "de_nivel_0",
    "de_nivel_1",
    "de_nivel_2",
    "de_nivel_3",
    "de_nivel_4",
    "para_id_classe",
    "para_nivel_0",
    "para_nivel_1",
    "para_nivel_2",
    "para_nivel_3",
    "para_nivel_4",
    "area"
FROM "base-dos-dados-br-mapbiomas-estatisticas--transicao-estado-bioma-de-para-quinquenal"
