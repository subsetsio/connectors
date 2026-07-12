-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grande_categorie_de_mesures",
    "categorie_de_mesures",
    "mesure_d_exoneration",
    "annee",
    CAST("code_grande_categorie_de_mesures" AS BIGINT) AS code_grande_categorie_de_mesures,
    CAST("code_categorie_de_mesures" AS BIGINT) AS code_categorie_de_mesures,
    CAST("code_mesure_d_exoneration" AS BIGINT) AS code_mesure_d_exoneration,
    "montant_des_exonerations"
FROM "urssaf-exos-secteur-prive-france-entiere-par-mesures"
