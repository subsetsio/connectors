-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "id_estado",
    "nom_estado",
    "nom_modalidadeoperacao",
    "nom_agenteproprietario",
    "id_tipousina",
    "id_usina",
    "nom_usina",
    "ceg",
    "cod_equipamento",
    "num_unidadegeradora",
    "nom_unidadegeradora",
    "val_potencia",
    "din_ano",
    "val_dispf",
    "val_indisppf",
    "val_indispff",
    "val_dmdff",
    "val_fdff",
    "val_tdff"
FROM "ons-brazil-ind-disponibilidade-fgeracao-uge-anual"
