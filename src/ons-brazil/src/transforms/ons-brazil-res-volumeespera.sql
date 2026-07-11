-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "tip_reservatorio",
    "nom_bacia",
    "nom_ree",
    "id_reservatorio",
    "nom_reservatorio",
    "num_ordemcs",
    "cod_usina",
    "din_instante",
    "val_volumeespera"
FROM "ons-brazil-res-volumeespera"
