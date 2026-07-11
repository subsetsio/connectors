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
    "nom_tipousina",
    "id_conjuntousina",
    "id_ons_conjunto",
    "id_ons_usina",
    "nom_conjunto",
    "nom_usina",
    "ceg",
    strptime("dat_iniciorelacionamento", '%Y-%m-%d')::DATE AS dat_iniciorelacionamento,
    "dat_fimrelacionamento"
FROM "ons-brazil-usina-conjunto"
