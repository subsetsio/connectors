-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nom_pais",
    "nom_agente",
    "nom_bloco",
    "din_instante",
    "val_importacaoprogramada",
    "val_importacaodespachada",
    "val_importacaoverificada",
    "val_preco"
FROM "ons-brazil-importacaoenergia-comercial-2"
