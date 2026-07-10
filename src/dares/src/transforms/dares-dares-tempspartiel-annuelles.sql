-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("date" AS BIGINT) AS date,
    "champ",
    "indicateur",
    "sexe",
    "age",
    "secteur",
    "pcs",
    "valeur"
FROM "dares-dares-tempspartiel-annuelles"
