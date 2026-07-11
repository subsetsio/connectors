-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "tip_reservatorio",
    "nom_bacia",
    "id_reservatorio",
    "nom_reservatorio",
    "cod_usina",
    "din_instante",
    "val_nivelmontante",
    "val_niveljusante",
    "val_volumeutil",
    "val_vazaoafluente",
    "val_vazaodefluente",
    "val_vazaoturbinada",
    "val_vazaovertida",
    "val_vazaooutrasestruturas",
    "val_vazaotransferida",
    "val_vazaovertidanaoturbinavel"
FROM "ons-brazil-dados-hidrologicos-ho"
