-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nom_conversora",
    "din_instante",
    CAST("val_modalidadecontratual" AS DOUBLE) AS val_modalidadecontratual,
    CAST("val_modalidadeemergencial" AS DOUBLE) AS val_modalidadeemergencial,
    CAST("val_modalidadeoportunidade" AS DOUBLE) AS val_modalidadeoportunidade,
    CAST("val_modalidadeteste" AS DOUBLE) AS val_modalidadeteste,
    CAST("val_modalidadeexcepcional" AS DOUBLE) AS val_modalidadeexcepcional,
    "nom_paisconversora",
    CAST("val_progmodalidadecontratual" AS DOUBLE) AS val_progmodalidadecontratual,
    CAST("val_progmodalidadeemergencial" AS DOUBLE) AS val_progmodalidadeemergencial,
    CAST("val_progmodalidadeoportunidade" AS DOUBLE) AS val_progmodalidadeoportunidade,
    CAST("val_progmodalidadeteste" AS DOUBLE) AS val_progmodalidadeteste,
    CAST("val_totalprogramado" AS DOUBLE) AS val_totalprogramado,
    CAST("val_totalverificado" AS DOUBLE) AS val_totalverificado
FROM "ons-brazil-intercambio-modalidade"
