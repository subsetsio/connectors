-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "id_estado",
    "nom_estado",
    "nom_agente_principal",
    "id_subestacao",
    "nom_subestacao",
    "val_niveltensao",
    "id_estacao",
    "num_barra",
    "val_latitude",
    "val_longitude"
FROM "ons-brazil-subestacao"
