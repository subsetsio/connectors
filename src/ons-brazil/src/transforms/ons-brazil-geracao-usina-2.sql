-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "din_instante",
    "id_subsistema",
    "nom_subsistema",
    "id_estado",
    "nom_estado",
    "cod_modalidadeoperacao",
    "nom_tipousina",
    "nom_tipocombustivel",
    "nom_usina",
    "id_ons",
    "ceg",
    "val_geracao"
FROM "ons-brazil-geracao-usina-2"
