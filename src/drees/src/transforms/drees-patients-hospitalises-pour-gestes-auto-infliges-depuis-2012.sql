-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "champ",
    "unite",
    "sexe",
    CAST("age" AS BIGINT) AS age,
    "nombre",
    "population",
    "taux"
FROM "drees-patients-hospitalises-pour-gestes-auto-infliges-depuis-2012"
