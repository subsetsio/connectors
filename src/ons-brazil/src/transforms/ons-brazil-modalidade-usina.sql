-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nom_usina",
    "ceg",
    "nom_modalidadeoperacao",
    "val_potenciaautorizada",
    "sgl_centrooperacao",
    "nom_pontoconexao",
    "id_estado",
    "nom_estado",
    "sts_aneel",
    "id_ons"
FROM "ons-brazil-modalidade-usina"
