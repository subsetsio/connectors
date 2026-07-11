-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cod_perturbacao",
    "din_interrupcaocarga",
    "id_subsistema",
    "nom_subsistema",
    "id_estado",
    "nom_agente",
    "val_cargainterrompida_mw",
    "val_tempomedio_minutos",
    "val_energianaosuprida_mwh",
    "flg_envolveuredebasica",
    "flg_envolveuredeoperacao"
FROM "ons-brazil-interrupcao-carga"
