-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "POLLUANT" AS polluant,
    "POURC_STATION_DEP_GDE_AGGLO" AS pourc_station_dep_gde_agglo,
    "POURC_STATION_DEP_AGGLO_MOY" AS pourc_station_dep_agglo_moy
FROM "sdes-9def3d04-67ed-4469-9d4a-2ab57fad95bb"
