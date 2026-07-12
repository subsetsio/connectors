-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "ancienne_region",
    "grande_categorie_de_mesures",
    "categorie_detail_ag",
    "annee",
    "code_region",
    "code_ancienne_region",
    CAST("code_grande_categorie_de_mesures" AS BIGINT) AS code_grande_categorie_de_mesures,
    CAST("code_categorie_detail_ag" AS BIGINT) AS code_categorie_detail_ag,
    "montant_des_exonerations"
FROM "urssaf-exos-secteur-prive-par-region-grandes-categories"
