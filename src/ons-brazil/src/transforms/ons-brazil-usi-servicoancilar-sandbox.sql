-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dat_verificada",
    "hor_verificada",
    "cod_pontoconexao",
    "ceg",
    "nom_conjunto",
    "val_must",
    CAST("flg_cpsa" AS BIGINT) AS flg_cpsa,
    "dsc_comentario"
FROM "ons-brazil-usi-servicoancilar-sandbox"
