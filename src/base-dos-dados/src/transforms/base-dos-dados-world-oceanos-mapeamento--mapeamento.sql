-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "titulo",
    "genero_literario",
    "outros_generos_literarios",
    "registro_linguistico",
    "tematica",
    "espaco_representacao",
    "ambiente_predominante",
    "temporalidade",
    "foco_narrativo",
    "tipo_narrador",
    "procedimento_expressivo",
    "genero_dramaturgico",
    "interprete",
    "narrador",
    "formato_cena",
    "estetica_cenografica",
    "tipo_localizacao",
    "localizacao_geografica"
FROM "base-dos-dados-world-oceanos-mapeamento--mapeamento"
