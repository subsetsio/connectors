-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grupo",
    "ordem",
    "familia",
    "especie_ou_subespecie",
    "categoria",
    "lista_2014"
FROM "base-dos-dados-br-mma-extincao--fauna-ameacada"
