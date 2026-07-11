-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "din_instante",
    "val_itaipu_total",
    "val_itaipu_60hz",
    "val_itaipu_50hz",
    "val_itaipu_50hz_br",
    "val_itaipu_br",
    "val_itaipu_py"
FROM "ons-brazil-geracao-itaipu"
