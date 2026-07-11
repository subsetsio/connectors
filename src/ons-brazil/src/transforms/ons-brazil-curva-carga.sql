-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verified row identity includes the load value because duplicate timestamps and subsystems can occur without another exposed discriminator.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "din_instante",
    "val_cargaenergiahomwmed"
FROM "ons-brazil-curva-carga"
