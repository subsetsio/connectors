-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "secteur_na38i",
    "secteur_na17i",
    "grand_secteur_d_activite",
    "grande_categorie_de_mesures",
    "categorie_detail_ag",
    "annee",
    CAST("code_grande_categorie_de_mesures" AS BIGINT) AS code_grande_categorie_de_mesures,
    CAST("code_categorie_detail_ag" AS BIGINT) AS code_categorie_detail_ag,
    "montant_des_exonerations"
FROM "urssaf-exos-secteur-na38i-grandes-categories"
