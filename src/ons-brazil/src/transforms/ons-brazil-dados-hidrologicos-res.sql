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
    "nom_reservatorio",
    "num_ordemcs",
    "cod_usina",
    "din_instante",
    "val_nivelmontante",
    "val_niveljusante",
    "val_volumeutilcon",
    "val_vazaoafluente",
    "val_vazaoturbinada",
    "val_vazaovertida",
    "val_vazaooutrasestruturas",
    "val_vazaodefluente",
    "val_vazaotransferida",
    "val_vazaonatural",
    "val_vazaoartificial",
    "val_vazaoincremental",
    "val_vazaoevaporacaoliquida",
    "val_vazaousoconsuntivo",
    "id_reservatorio",
    "val_vazaoincrementalbruta"
FROM "ons-brazil-dados-hidrologicos-res"
