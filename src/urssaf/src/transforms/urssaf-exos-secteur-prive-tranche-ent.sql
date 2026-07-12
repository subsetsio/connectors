-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tranche_d_effectif",
    "grande_categorie_de_mesures",
    "categorie_de_mesures",
    "annee",
    CAST("code_grande_categorie_de_mesures" AS BIGINT) AS code_grande_categorie_de_mesures,
    CAST("code_categorie_de_mesures" AS BIGINT) AS code_categorie_de_mesures,
    "montant_des_exonerations"
FROM "urssaf-exos-secteur-prive-tranche-ent"
