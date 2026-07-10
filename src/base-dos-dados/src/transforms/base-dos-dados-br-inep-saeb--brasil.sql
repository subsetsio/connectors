-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "rede",
    "localizacao",
    "disciplina",
    "serie",
    "media",
    "nivel_0",
    "nivel_1",
    "nivel_2",
    "nivel_3",
    "nivel_4",
    "nivel_5",
    "nivel_6",
    "nivel_7",
    "nivel_8",
    "nivel_9",
    "nivel_10"
FROM "base-dos-dados-br-inep-saeb--brasil"
