-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "id_estado",
    "nom_estado",
    "nom_usina",
    "id_tipousina",
    "nom_tipocombustivel",
    "id_ons",
    "ceg",
    "din_instante",
    CAST("val_potenciainstalada" AS DOUBLE) AS val_potenciainstalada,
    CAST("val_dispoperacional" AS DOUBLE) AS val_dispoperacional,
    CAST("val_dispsincronizada" AS DOUBLE) AS val_dispsincronizada
FROM "ons-brazil-disponibilidade-usina"
