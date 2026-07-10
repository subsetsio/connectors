-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sigla_uf",
    "ano",
    "mes",
    "automovel",
    "bonde",
    "caminhao",
    "caminhaotrator",
    "caminhonete",
    "camioneta",
    "chassiplataforma",
    "ciclomotor",
    "microonibus",
    "motocicleta",
    "motoneta",
    "onibus",
    "quadriciclo",
    "reboque",
    "semireboque",
    "sidecar",
    "outros",
    "tratoresteira",
    "tratorrodas",
    "triciclo",
    "utilitario",
    "total"
FROM "base-dos-dados-br-denatran-frota--uf-tipo"
