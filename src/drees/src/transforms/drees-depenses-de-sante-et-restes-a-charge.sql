-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "variable",
    "poste",
    "classe_d_age",
    "sexe",
    "ald",
    "c2s",
    "echantillon",
    "valeur",
    "nombre_de_consommants"
FROM "drees-depenses-de-sante-et-restes-a-charge"
