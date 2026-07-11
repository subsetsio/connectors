-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "nom_bacia",
    "nom_rio",
    "nom_agente",
    "nom_reservatorio",
    "cod_usina",
    "din_instante",
    CAST("val_geracao" AS DOUBLE) AS val_geracao,
    CAST("val_disponibilidade" AS DOUBLE) AS val_disponibilidade,
    CAST("val_vazaoturbinada" AS DOUBLE) AS val_vazaoturbinada,
    CAST("val_vazaovertida" AS DOUBLE) AS val_vazaovertida,
    CAST("val_vazaovertidanaoturbinavel" AS DOUBLE) AS val_vazaovertidanaoturbinavel,
    CAST("val_produtividade" AS DOUBLE) AS val_produtividade,
    CAST("val_folgadegeracao" AS DOUBLE) AS val_folgadegeracao,
    CAST("val_energiavertida" AS DOUBLE) AS val_energiavertida,
    CAST("val_vazaovertidaturbinavel" AS DOUBLE) AS val_vazaovertidaturbinavel,
    CAST("val_energiavertidaturbinavel" AS DOUBLE) AS val_energiavertidaturbinavel
FROM "ons-brazil-energia-vertida-turbinavel"
