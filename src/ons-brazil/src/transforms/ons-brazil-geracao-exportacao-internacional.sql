-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "din_instante",
    "val_gerexpevt_ar",
    "val_gerexpevt_uy",
    "val_gerexptermica",
    "val_exportacao_ar",
    "val_exportacao_uy"
FROM "ons-brazil-geracao-exportacao-internacional"
