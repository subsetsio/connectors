-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "champ",
    "grande_categorie_de_mesures",
    "annee",
    CAST("code_grande_categorie_de_mesures" AS BIGINT) AS code_grande_categorie_de_mesures,
    "montant_des_exonerations"
FROM "urssaf-exos-champ-large-par-grandes-categories"
