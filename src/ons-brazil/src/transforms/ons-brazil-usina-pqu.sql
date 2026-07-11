-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "estad_id",
    "nom_estado",
    "id_tipousina",
    "id_ons_pequenasusinas",
    "id_ons_usina",
    "nom_pequenasusinas",
    "nom_usina",
    "ceg"
FROM "ons-brazil-usina-pqu"
